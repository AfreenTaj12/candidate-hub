from fastapi import FastAPI

from database import engine, Base
import models
from routers.auth import router as auth_router
from routers.candidates import router as candidates_router
from routers.jobs import router as jobs_router
from routers.applications import router as applications_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="CandidateHub API",
    description="Mini Candidate Job Portal",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://localhost:5173",
    "https://candidate-hub-umber.vercel.app"
],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(candidates_router)
app.include_router(jobs_router)
app.include_router(applications_router)
@app.get("/")
def home():
    return {"message": "Welcome to CandidateHub API"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}