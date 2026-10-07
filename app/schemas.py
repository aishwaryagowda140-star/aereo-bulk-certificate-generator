from datetime import date

from pydantic import BaseModel, EmailStr, Field


class RecipientCreate(BaseModel):
    name: str = Field(..., min_length=2)
    email: EmailStr


class GenerationJobCreate(BaseModel):
    event_name: str = Field(..., min_length=2)
    event_date: date
    recipients: list[RecipientCreate] = Field(..., min_length=1)


class JobResponse(BaseModel):
    job_id: int
    status: str
    total: int
    successful: int
    failed: int


class CertificateResponse(BaseModel):
    id: int
    recipient_name: str
    recipient_email: str
    status: str
    file_path: str | None = None
    error_message: str | None = None