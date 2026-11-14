from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base


class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), nullable=False)
    company = Column(String(150), nullable=False)
    location = Column(String(150))
    description = Column(String)
    job_type = Column(String(50))


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"))
    job_id = Column(Integer, ForeignKey("jobs.id"))
    status = Column(String(50), default="Applied")
    applied_at = Column(DateTime(timezone=True), server_default=func.now())