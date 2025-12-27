from pydantic import BaseModel, HttpUrl


class JobCreate(BaseModel):
    schedule: str
    api: HttpUrl
    type: str = "ATLEAST_ONCE"


class JobResponse(BaseModel):
    job_id: str

