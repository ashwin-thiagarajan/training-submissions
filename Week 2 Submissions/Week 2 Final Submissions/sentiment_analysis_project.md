# Week 2 Final Assignment: Sentiment Analysis API

## Objective

Build a production-style Django REST API for sentiment analysis using the provided Django REST API guide as the base reference.

Reference guide:

```text
/Users/ravikanth.boggavarapu/Library/CloudStorage/OneDrive-QuadraticInsightsPvtLtd/Projects/Q Arch Team/DjangoAPP/Django_REST_API_Guide.md
```

## Submission Folder

```text
week2_sentiment_analysis_submission/
```

Starter code is available under:

```text
week2_training/final_assignment/starter_template/sentiment_analysis_django/
```

Reference templates are available under:

```text
week2_training/standard_templates/django_qtx_reference/
week2_training/standard_templates/fastapi_sentiment_analysis_reference/
```

Use the Django reference for this assignment's project structure. Use the FastAPI reference only to compare service/schema/test organization patterns.

## Required API

| Method | Path | Behavior |
| --- | --- | --- |
| `POST` | `/api/v1/sentiment-analysis/` | Return sentiment label and score for input text |
| `GET` | `/health/` | Return API health status |

## Request Body

```json
{
  "text": "I love this product! It is amazing."
}
```

## Success Response

```json
{
  "text": "I love this product! It is amazing.",
  "sentiment": "Positive",
  "score": 0.98
}
```

## Technical Requirements

- Use Django REST Framework.
- Authentication is optional.
- Do not use Django ORM for this assignment.
- Use Pydantic for request validation.
- Maintain `.env.example`; do not commit `.env`.
- Keep model name and log level configurable through environment variables.
- Maintain clean files: `schemas.py`, `services.py`, `views.py`, `urls.py`, `exceptions.py`, and tests.
- Use `logging.getLogger(__name__)`.
- Use specific exception handling.
- Return correct status codes.
- Return structured error responses.
- Add Docker support.
- Add unit tests.

## Validation Requirements

- `text` is required.
- `text` must be a strict string.
- `text` length must be between 2 and 5000 characters.
- Extra fields must be rejected.

## Required Tests

- Valid sentiment request returns `200`.
- Missing text returns `400`.
- Empty text returns `400`.
- Extra field returns `400`.
- Service inference failure returns structured `500`.
- `/health/` returns `200`.

## Expected Error Response

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request payload.",
    "details": []
  }
}
```

## Evaluation Criteria

| Area | Weight |
| --- | ---: |
| Project structure | 15% |
| Pydantic validation | 20% |
| Sentiment service implementation | 20% |
| Config and `.env.example` handling | 10% |
| Logging and exception handling | 10% |
| Status codes and error shape | 10% |
| Unit tests | 15% |

## Submission Checklist

- `requirements.txt` exists.
- `.env.example` exists.
- `.env` is not submitted.
- API runs locally.
- Tests pass.
- Docker image builds.
- No hardcoded secrets, hostnames, or model config.
- No `print()` statements in API code.
