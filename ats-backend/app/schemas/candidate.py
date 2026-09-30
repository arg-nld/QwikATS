from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CandidateCreate(BaseModel):
    tenant_id: int
    first_name: str
    last_name: str
    email: str
    phone: str | None = None
    resume_url: str | None = None
    resume_text: str | None = None
    skills: str = ""
    experience_years: int = 0


class CandidateUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    phone: str | None = None
    resume_url: str | None = None
    resume_text: str | None = None
    skills: str | None = None
    experience_years: int | None = None


class CandidateResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    tenant_id: int
    first_name: str
    last_name: str
    email: str
    phone: str | None
    resume_url: str | None
    resume_text: str | None
    skills: str
    experience_years: int
    created_at: datetime
    updated_at: datetime