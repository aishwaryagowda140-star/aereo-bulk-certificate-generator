from fastapi import BackgroundTasks, FastAPI, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from . import models
from .schemas import (
    GenerationJobCreate,
    JobResponse,
    CertificateResponse
)
from .services import process_generation_job


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Bulk Certificate Generator API",
    description="Backend API for bulk certificate generation",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Bulk Certificate Generator API is running"
    }


@app.post("/api/jobs/", response_model=JobResponse)
def create_generation_job(
    request: GenerationJobCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    job = models.GenerationJob(
        event_name=request.event_name,
        event_date=str(request.event_date),
        status="PENDING",
        total=len(request.recipients),
        successful=0,
        failed=0
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    for recipient in request.recipients:
        certificate = models.Certificate(
            job_id=job.id,
            recipient_name=recipient.name,
            recipient_email=recipient.email,
            status="PENDING"
        )

        db.add(certificate)

    db.commit()

    background_tasks.add_task(
        process_generation_job,
        job.id
    )

    return JobResponse(
        job_id=job.id,
        status=job.status,
        total=job.total,
        successful=job.successful,
        failed=job.failed
    )


@app.get("/api/jobs/{job_id}", response_model=JobResponse)
def get_job_status(
    job_id: int,
    db: Session = Depends(get_db)
):
    job = db.query(models.GenerationJob).filter(
        models.GenerationJob.id == job_id
    ).first()

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    return JobResponse(
        job_id=job.id,
        status=job.status,
        total=job.total,
        successful=job.successful,
        failed=job.failed
    )


@app.get(
    "/api/jobs/{job_id}/certificates/",
    response_model=list[CertificateResponse]
)
def get_job_certificates(
    job_id: int,
    db: Session = Depends(get_db)
):
    job = db.query(models.GenerationJob).filter(
        models.GenerationJob.id == job_id
    ).first()

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    certificates = db.query(models.Certificate).filter(
        models.Certificate.job_id == job_id
    ).all()

    return certificates


@app.get("/api/certificates/{certificate_id}/download")
def download_certificate(
    certificate_id: int,
    db: Session = Depends(get_db)
):
    certificate = db.query(models.Certificate).filter(
        models.Certificate.id == certificate_id
    ).first()

    if not certificate:
        raise HTTPException(
            status_code=404,
            detail="Certificate not found"
        )

    if certificate.status != "SUCCESS":
        raise HTTPException(
            status_code=400,
            detail="Certificate is not ready"
        )

    return FileResponse(
        certificate.file_path,
        media_type="application/pdf",
        filename=f"certificate_{certificate.id}.pdf"
    )