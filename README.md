> Assignment: High-Throughput Job Scheduler (Segment B – B1.0)

# High-Throughput Job Scheduler

This project implements a simple, scalable job scheduler capable of executing scheduled HTTP jobs with at-least-once semantics. The system supports job creation, scheduled execution, execution tracking, and basic observability.

The focus of this implementation is clarity of design, correctness, and thoughtful trade-offs.

## Architecture Overview

The system is composed of the following components:

- **API Layer (FastAPI)**  
  Exposes endpoints to create jobs and query execution history.

- **Scheduler (APScheduler)**  
  Triggers jobs based on a cron schedule with second-level precision.

- **Execution Worker**  
  Executes HTTP POST requests and records execution outcomes.

- **Persistence Layer (SQLite)**  
  Stores job definitions and execution history.

- **Observability**  
  Basic logging and execution visibility through APIs.

## API Endpoints

### Create Job
`POST /jobs`

Accepts a job specification including:
- Cron schedule (with seconds)
- API endpoint
- Execution type (ATLEAST_ONCE)

Returns a unique `job_id`.

### Get Job Executions
`GET /jobs/{job_id}/executions`

Returns the last 5 execution records for a given job, including:
- Execution timestamp
- Status (SUCCESS / FAILED)
- HTTP response status
- Execution duration

## Data Model

### Job
- job_id (UUID)
- schedule (cron string)
- api_endpoint (URL)
- type
- created_at

### JobExecution
- execution_id
- job_id
- timestamp
- status
- http_status
- duration_ms

## Execution Flow

1. A job is created via the API and persisted in the database.
2. The scheduler registers the job using a cron trigger with second-level precision.
3. At each scheduled time, the job is executed as an HTTP POST request.
4. Each execution is recorded with status, duration, and response metadata.
5. On failure, the job is retried once to satisfy at-least-once semantics.

## Trade-offs & Design Decisions

- **SQLite** was chosen for simplicity and ease of setup. In a production system, this could be replaced with a distributed database.
- **APScheduler** was used for scheduling. Since `from_crontab` does not support seconds, cron fields were explicitly parsed to enable second-level scheduling.
- **At-least-once semantics** are implemented via a simple retry mechanism (two attempts).
- The system prioritizes correctness and clarity over high availability or horizontal scaling.

## Limitations & Future Improvements

- No support for high availability or leader election.
- No distributed execution or worker pool.
- Alerting is limited to logs and execution visibility.
- Retry logic is minimal and could be enhanced with backoff strategies.
- Metrics could be extended using Prometheus or similar tooling.

## How to Run

1. Create and activate a virtual environment
2. Install dependencies: pip install -r requirements.txt
3. Start the server: uvicorn app.main:app --reload
4. Open Swagger UI: http://127.0.0.1:8000/docs

## Experience Working on This Problem

This assignment required balancing system design with practical implementation under time constraints. The most interesting aspect was handling scheduling precision and execution guarantees while keeping the system simple and explainable. With more time, the system could be extended for higher availability and scale.


