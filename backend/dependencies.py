import os
import jwt

from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session

from database import get_db
from models import Candidate

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

security = HTTPBearer()


def get_current_candidate(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        candidate_id = int(payload.get("sub"))

    except (InvalidTokenError, TypeError, ValueError):
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    candidate = db.query(Candidate).filter(
        Candidate.id == candidate_id
    ).first()

    if candidate is None:
        raise HTTPException(
            status_code=401,
            detail="Candidate not found"
        )

    return candidate