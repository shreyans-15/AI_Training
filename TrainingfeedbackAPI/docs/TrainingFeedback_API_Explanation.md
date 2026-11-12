# Corporate Training Feedback API — Assignment Explanation

## Problem and objective
The API supports a corporate training feedback platform to assess training sessions, trainer quality, and learner satisfaction. It uses FastAPI, Pydantic, SQLAlchemy ORM, and MySQL.

## Data model
`TrainingFeedback` stores:
- `feedback_id`: unique integer identifier
- `learner_name`, `trainer_name`, `course_name`: required text fields
- `session_date`: date
- `content_rating`, `trainer_rating`, `hands_on_rating`: integers from 1 to 5
- `comments`: optional text
- `would_recommend`: boolean

## Endpoints
1. `POST /feedback/` — submit a feedback record.
2. `GET /feedback/` — list records using `skip` and `limit`.
3. `GET /feedback/{feedback_id}` — retrieve a record by ID.
4. `PUT /feedback/{feedback_id}` — update one or more supplied fields.
5. `DELETE /feedback/{feedback_id}` — delete a record.
6. `GET /feedback/by-trainer/{trainer_name}` — filter by trainer.
7. `GET /feedback/by-course/{course_name}` — filter by course.
8. `GET /feedback/average-trainer-ratings` — calculate average trainer rating grouped by trainer.
9. `GET /feedback/low-rated` — find records where at least one of the three ratings is 2 or below.
10. `GET /feedback/recommendation-percentage?course_name=...` — calculate the share of course feedback that recommends the course.

## Validation and exceptions
Pydantic enforces ratings from 1 to 5. Duplicate feedback IDs return 409. Missing feedback returns 404. Invalid request data returns 422. Database exceptions trigger rollback where applicable, are recorded in logs, and return a generic 500 response. A course with no feedback returns zero percent and zero total rather than dividing by zero.

## Logging
The application writes to `logs/app.log` with timestamp, level, logger name, and message. Successful create/update/delete operations are INFO; duplicate IDs and missing records are WARNING; unexpected database errors are logged with traceback using `logger.exception()`.

## Testing evidence to add after running
Add actual Swagger request/response screenshots for all ten operations, at least four error scenarios, and log-file evidence. Do not present sample screenshots or sample responses as actual test evidence.
