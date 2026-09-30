from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict


class ApplicationStatus(str, Enum):
    APPLIED = "applied"
    SCREENING = "screening"
    INTERVIEW = "interview"
    OFFER = "offer"
    HIRED = "hired"
    REJECTED = "rejected"


class ApplicationCreate(BaseModel):
    tenant_id: int
    candidate_id: int
    job_id: int
    status: ApplicationStatus = ApplicationStatus.APPLIED


class ApplicationUpdate(BaseModel):
    status: ApplicationStatus


class ApplicationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    tenant_id: int
    candidate_id: int
    job_id: int
    status: ApplicationStatus
    created_at: datetime
    updated_at: datetime