from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Job
from app.services.job_executor import execute_job

scheduler = BackgroundScheduler()


def schedule_job(job: Job):
    # Split cron fields
    fields = job.schedule.split()

    if len(fields) != 6:
        raise ValueError("Cron schedule must have 6 fields (including seconds)")

    second, minute, hour, day, month, day_of_week = fields

    trigger = CronTrigger(
        second=second,
        minute=minute,
        hour=hour,
        day=day,
        month=month,
        day_of_week=day_of_week
    )

    def job_wrapper():
        db: Session = SessionLocal()
        try:
            execute_job(db, job)
        finally:
            db.close()

    scheduler.add_job(
        job_wrapper,
        trigger=trigger,
        id=job.job_id,
        replace_existing=True
    )
