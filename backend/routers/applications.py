from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Application, Job, Candidate
from dependencies import get_current_candidate

router = APIRouter(prefix="/applications", tags=["Applications"])


@router.post("/{job_id}")
def apply_for_job(
    job_id: int,
    current_candidate: Candidate = Depends(get_current_candidate),
    db: Session = Depends(get_db)
):
    job = db.query(Job).filter(Job.id == job_id).first()

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    existing_application = db.query(Application).filter(
        Application.candidate_id == current_candidate.id,
        Application.job_id == job_id
    ).first()

    if existing_application:
        raise HTTPException(
            status_code=400,
            detail="You have already applied for this job"
        )

    new_application = Application(
        candidate_id=current_candidate.id,
        job_id=job_id,
        status="Applied"
    )

    db.add(new_application)
    db.commit()
    db.refresh(new_application)

    return {
        "message": "Application submitted successfully",
        "application_id": new_application.id,
        "status": new_application.status
    }


@router.get("/me")
def get_my_applications(
    current_candidate: Candidate = Depends(get_current_candidate),
    db: Session = Depends(get_db)
):
    applications = db.query(Application).filter(
        Application.candidate_id == current_candidate.id
    ).all()

    return applications