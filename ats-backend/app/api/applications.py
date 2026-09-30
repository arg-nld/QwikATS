from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.application import Application
from app.models.candidate import Candidate
from app.models.job import Job
from app.models.tenant import Tenant
from app.schemas.application import (
    ApplicationCreate,
    ApplicationResponse,
    ApplicationUpdate,
)


router = APIRouter(
    prefix="/api/applications",
    tags=["Applications"],
)


@router.get(
    "/",
    response_model=list[ApplicationResponse],
)
def get_applications(
    tenant_id: int | None = None,
    candidate_id: int | None = None,
    job_id: int | None = None,
    status: str | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(Application)

    if tenant_id is not None:
        query = query.filter(
            Application.tenant_id == tenant_id
        )

    if candidate_id is not None:
        query = query.filter(
            Application.candidate_id == candidate_id
        )

    if job_id is not None:
        query = query.filter(
            Application.job_id == job_id
        )

    if status is not None:
        query = query.filter(
            Application.status == status
        )

    return query.all()


@router.get(
    "/{application_id}",
    response_model=ApplicationResponse,
)
def get_application(
    application_id: int,
    db: Session = Depends(get_db),
):
    application = (
        db.query(Application)
        .filter(Application.id == application_id)
        .first()
    )

    if not application:
        raise HTTPException(
            status_code=404,
            detail="Application not found",
        )

    return application


@router.post(
    "/",
    response_model=ApplicationResponse,
    status_code=201,
)
def create_application(
    application_data: ApplicationCreate,
    db: Session = Depends(get_db),
):
    tenant = (
        db.query(Tenant)
        .filter(Tenant.id == application_data.tenant_id)
        .first()
    )

    if not tenant:
        raise HTTPException(
            status_code=404,
            detail="Tenant not found",
        )

    candidate = (
        db.query(Candidate)
        .filter(
            Candidate.id == application_data.candidate_id,
            Candidate.tenant_id == application_data.tenant_id,
        )
        .first()
    )

    if not candidate:
        raise HTTPException(
            status_code=404,
            detail="Candidate not found for this tenant",
        )

    job = (
        db.query(Job)
        .filter(
            Job.id == application_data.job_id,
            Job.tenant_id == application_data.tenant_id,
        )
        .first()
    )

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found for this tenant",
        )

    application = Application(
        **application_data.model_dump()
    )

    db.add(application)
    db.commit()
    db.refresh(application)

    return application


@router.put(
    "/{application_id}",
    response_model=ApplicationResponse,
)
def update_application(
    application_id: int,
    application_data: ApplicationUpdate,
    db: Session = Depends(get_db),
):
    application = (
        db.query(Application)
        .filter(Application.id == application_id)
        .first()
    )

    if not application:
        raise HTTPException(
            status_code=404,
            detail="Application not found",
        )

    application.status = application_data.status

    db.commit()
    db.refresh(application)

    return application