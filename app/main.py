from app.scheduler import scheduler, schedule_job
from app.models import Job
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.database import engine, get_db
from app.models import Base
from app.schemas import JobCreate, JobResponse
from app.services.job_service import create_job

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Job Scheduler")


@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/jobs", response_model=JobResponse)
def create_job_api(job: JobCreate, db: Session = Depends(get_db)):
    created_job = create_job(db, job)
    schedule_job(created_job)
    return {"job_id": created_job.job_id}


@app.on_event("startup")
def start_scheduler():
    scheduler.start()

