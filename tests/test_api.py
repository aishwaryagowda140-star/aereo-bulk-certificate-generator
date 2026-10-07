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