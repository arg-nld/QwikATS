from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CandidateCreate(BaseModel):
    tenant_id: int
    first_name: str
    last_name: str
    email: str
    phone: str | None = None
    resume_url: str | None = None


class CandidateUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    phone: str | None = None
    resume_url: str | None = None


class CandidateResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    tenant_id: int
    first_name: str
    last_name: str
    email: str
    phone: str | None
    resume_url: str | None
    created_at: datetime
    updated_at: datetime