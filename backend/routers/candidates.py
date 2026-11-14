from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from dependencies import get_current_candidate
from models import Candidate
from schemas import CandidateProfileUpdate, CandidateProfileResponse

router = APIRouter(prefix="/candidates", tags=["Candidate Profile"])


@router.get("/me", response_model=CandidateProfileResponse)
def get_profile(
    current_candidate: Candidate = Depends(get_current_candidate)
):
    return current_candidate


@router.put("/me", response_model=CandidateProfileResponse)
def update_profile(
    profile: CandidateProfileUpdate,
    current_candidate: Candidate = Depends(get_current_candidate),
    db: Session = Depends(get_db)
):
    current_candidate.name = profile.name

    db.commit()
    db.refresh(current_candidate)

    return current_candidate