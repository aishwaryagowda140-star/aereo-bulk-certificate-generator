from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_create_generation_job():
    response = client.post(
        "/api/jobs/",
        json={
            "event_name": "Test Workshop",
            "event_date": "2026-10-07",
            "recipients": [
                {
                    "name": "Aishwarya",
                    "email": "aishwarya@example.com"
                },
                {
                    "name": "Rahul",
                    "email": "rahul@example.com"
                }
            ]
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "job_id" in data
    assert data["total"] == 2


def test_invalid_email():
    response = client.post(
        "/api/jobs/",
        json={
            "event_name": "Test Workshop",
            "event_date": "2026-10-07",
            "recipients": [
                {
                    "name": "Aishwarya",
                    "email": "invalid-email"
                }
            ]
        }
    )

    assert response.status_code == 422


def test_job_not_found():
    response = client.get("/api/jobs/999999")

    assert response.status_code == 404

from unittest.mock import patch

from app.database import SessionLocal
from app.models import GenerationJob, Certificate
from app.services import process_generation_job


def test_individual_certificate_failure():
    db = SessionLocal()

    job = GenerationJob(
        event_name="Failure Test",
        event_date="2026-10-07",
        status="PENDING",
        total=2,
        successful=0,
        failed=0
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    certificate1 = Certificate(
        job_id=job.id,
        recipient_name="Good User",
        recipient_email="good@example.com",
        status="PENDING"
    )

    certificate2 = Certificate(
        job_id=job.id,
        recipient_name="Bad User",
        recipient_email="bad@example.com",
        status="PENDING"
    )

    db.add_all([certificate1, certificate2])
    db.commit()

    def fake_generator(
        recipient_name,
        event_name,
        event_date,
        certificate_id
    ):
        if recipient_name == "Bad User":
            raise ValueError("Certificate generation failed")
        return "generated_certificates/test.pdf"

    with patch(
        "app.services.generate_certificate",
        side_effect=fake_generator
    ):
        process_generation_job(job.id)

    db.refresh(job)
    db.refresh(certificate1)
    db.refresh(certificate2)

    assert job.successful == 1
    assert job.failed == 1
    assert job.status == "COMPLETED_WITH_ERRORS"

    assert certificate1.status == "SUCCESS"
    assert certificate2.status == "FAILED"
    assert certificate2.error_message == "Certificate generation failed"

    db.delete(job)
    db.commit()
    db.close()