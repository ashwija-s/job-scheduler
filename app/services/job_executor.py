import time
import requests
from sqlalchemy.orm import Session
from app import models


def execute_job(db: Session, job: models.Job):
    start_time = time.time()
    status = "SUCCESS"
    http_status = None

    try:
        response = requests.post(job.api_endpoint, timeout=5)
        http_status = response.status_code
        if response.status_code >= 400:
            status = "FAILED"
    except Exception:
        status = "FAILED"

    duration_ms = int((time.time() - start_time) * 1000)

    execution = models.JobExecution(
        job_id=job.job_id,
        status=status,
        http_status=http_status,
        duration_ms=duration_ms
    )

    db.add(execution)
    db.commit()
