from datetime import datetime

from pydantic import BaseModel, ConfigDict


class JobBase(BaseModel):
    title: str
    description: str | None = None
    department: str | None = None
    location: str | None = None
    employment_type: str | None = None
    status: str = "draft"


class JobCreate(JobBase):
    tenant_id: int


class JobUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    department: str | None = None
    location: str | None = None
    employment_type: str | None = None
    status: str | None = None


class JobResponse(JobBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    tenant_id: int
    created_at: datetime
    updated_at: datetime