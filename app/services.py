from datetime import datetime

from .database import SessionLocal
from .models import GenerationJob, Certificate
from .certificate_generator import generate_certificate


def process_generation_job(job_id: int):
    db = SessionLocal()

    try:
        job = db.query(GenerationJob).filter(
            GenerationJob.id == job_id
        ).first()

        if not job:
            return

        job.status = "PROCESSING"
        db.commit()

        certificates = db.query(Certificate).filter(
            Certificate.job_id == job_id
        ).all()

        for certificate in certificates:
            try:
                if len(certificate.recipient_name.strip()) < 2:
                    raise ValueError(
                        "Recipient name must contain at least 2 characters"
                    )

                file_path = generate_certificate(
                    recipient_name=certificate.recipient_name,
                    event_name=job.event_name,
                    event_date=job.event_date,
                    certificate_id=certificate.id
                )

                certificate.status = "SUCCESS"
                certificate.file_path = file_path
                certificate.error_message = None

                job.successful += 1

            except Exception as error:
                certificate.status = "FAILED"
                certificate.error_message = str(error)

                job.failed += 1

            db.commit()

        if job.failed > 0:
            job.status = "COMPLETED_WITH_ERRORS"
        else:
            job.status = "COMPLETED"

        job.completed_at = datetime.utcnow()

        db.commit()

    finally:
        db.close()