import uuid
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey
from sqlalchemy.sql import func
from app.database import Base


class Job(Base):
    __tablename__ = "jobs"

    job_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    schedule = Column(String, nullable=False)
    api_endpoint = Column(String, nullable=False)
    type = Column(String, default="ATLEAST_ONCE")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class JobExecution(Base):
    __tablename__ = "executions"

    execution_id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String, ForeignKey("jobs.job_id"))
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String)
    http_status = Column(Integer, nullable=True)
    duration_ms = Column(Integer)
