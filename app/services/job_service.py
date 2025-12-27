from sqlalchemy.orm import Session
from app import models
from app.schemas import JobCreate


def create_job(db: Session, job: JobCreate):
    new_job = models.Job(
        schedule=job.schedule,
        api_endpoint=str(job.api),
        type=job.type
    )
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return new_job
