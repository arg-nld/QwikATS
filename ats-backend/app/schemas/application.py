from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ApplicationCreate(BaseModel):
    tenant_id: int
    candidate_id: int
    job_id: int
    status: str = "applied"


class ApplicationUpdate(BaseModel):
    status: str


class ApplicationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    tenant_id: int
    candidate_id: int
    job_id: int
    status: str
    created_at: datetime
    updated_at: datetime