from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.job import Job
from app.models.tenant import Tenant
from app.schemas.job import JobCreate, JobResponse, JobUpdate


router = APIRouter(
    prefix="/api/jobs",
    tags=["Jobs"],
)


@router.get("/", response_model=list[JobResponse])
def get_jobs(db: Session = Depends(get_db)):
    return db.query(Job).all()


@router.get("/{job_id}", response_model=JobResponse)
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found",
        )

    return job


@router.post("/", response_model=JobResponse, status_code=201)
def create_job(
    job_data: JobCreate,
    db: Session = Depends(get_db),
):
    tenant = (
        db.query(Tenant)
        .filter(Tenant.id == job_data.tenant_id)
        .first()
    )

    if not tenant:
        raise HTTPException(
            status_code=404,
            detail="Tenant not found",
        )

    job = Job(**job_data.model_dump())

    db.add(job)
    db.commit()
    db.refresh(job)

    return job


@router.put("/{job_id}", response_model=JobResponse)
def update_job(
    job_id: int,
    job_data: JobUpdate,
    db: Session = Depends(get_db),
):
    job = db.query(Job).filter(Job.id == job_id).first()

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found",
        )

    update_data = job_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(job, field, value)

    db.commit()
    db.refresh(job)

    return job


@router.delete("/{job_id}")
def delete_job(
    job_id: int,
    db: Session = Depends(get_db),
):
    job = db.query(Job).filter(Job.id == job_id).first()

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found",
        )

    db.delete(job)
    db.commit()

    return {
        "message": "Job deleted successfully"
    }