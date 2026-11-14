from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Candidate
from schemas import CandidateRegister, CandidateResponse
from auth import hash_password
import os
import jwt

from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

from schemas import CandidateLogin, TokenResponse
from auth import verify_password

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=CandidateResponse)
def register(candidate: CandidateRegister, db: Session = Depends(get_db)):

    existing_candidate = db.query(Candidate).filter(
        Candidate.email == candidate.email
    ).first()

    if existing_candidate:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    new_candidate = Candidate(
        name=candidate.name,
        email=candidate.email,
        hashed_password=hash_password(candidate.password)
    )

    db.add(new_candidate)
    db.commit()
    db.refresh(new_candidate)

    return new_candidate

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"


@router.post("/login", response_model=TokenResponse)
def login(candidate: CandidateLogin, db: Session = Depends(get_db)):

    existing_candidate = db.query(Candidate).filter(
        Candidate.email == candidate.email
    ).first()

    if not existing_candidate:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(
        candidate.password,
        existing_candidate.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    expire = datetime.now(timezone.utc) + timedelta(minutes=60)

    token = jwt.encode(
        {
            "sub": str(existing_candidate.id),
            "exp": expire
        },
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }