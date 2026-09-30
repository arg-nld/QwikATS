from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.candidate import Candidate
from app.models.job import Job
from app.services.scoring import calculate_compatibility


router = APIRouter(
    prefix="/api/scoring",
    tags=["Scoring"],
)


@router.get(
    "/jobs/{job_id}/candidates/{candidate_id}"
)
def score_candidate(
    job_id: int,
    candidate_id: int,
    db: Session = Depends(get_db),
):
    job = (
        db.query(Job)
        .filter(Job.id == job_id)
        .first()
    )

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found",
        )

    candidate = (
        db.query(Candidate)
        .filter(
            Candidate.id == candidate_id,
            Candidate.tenant_id == job.tenant_id,
        )
        .first()
    )

    if not candidate:
        raise HTTPException(
            status_code=404,
            detail="Candidate not found for this job",
        )

    result = calculate_compatibility(
        job,
        candidate,
    )

    return {
        "job_id": job.id,
        "candidate_id": candidate.id,
        "candidate_name": (
            f"{candidate.first_name} "
            f"{candidate.last_name}"
        ),
        **result,
    }