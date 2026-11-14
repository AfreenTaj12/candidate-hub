from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Job

router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.get("/")
def get_jobs(
    search: str = None,
    location: str = None,
    job_type: str = None,
    db: Session = Depends(get_db)
):
    query = db.query(Job)

    if search:
        query = query.filter(Job.title.ilike(f"%{search}%"))

    if location:
        query = query.filter(Job.location.ilike(f"%{location}%"))

    if job_type:
        query = query.filter(Job.job_type.ilike(f"%{job_type}%"))

    return query.all()


@router.get("/{job_id}")
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    return job