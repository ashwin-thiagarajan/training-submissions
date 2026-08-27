# Week 2 API Quality Checklist

Use this checklist for every Django REST Framework and FastAPI task.

## Mandatory Standards

- Keep secrets and environment-specific values in `.env`; commit only `.env.example`.
- Centralize configuration in `config.py`, `settings.py`, or a Pydantic settings class.
- Use clear project structure: routes/views, schemas/serializers, services, config, tests.
- Validate every request body before business logic runs.
- Use Pydantic models for request and service DTO validation in Week 2 exercises.
- Return structured response bodies for success and error cases.
- Use correct HTTP status codes.
- Use `logging.getLogger(__name__)`; do not use `print()` in API code.
- Catch specific exceptions at API boundaries and return user-friendly errors.
- Never return stack traces or internal exception messages to API clients.
- Keep business logic in services so it can be unit tested.
- Write unit tests for success, validation failure, not found, and internal failure paths.
- Use type hints for function parameters and return values.
- Pin or constrain dependency versions in `requirements.txt`.

## Django REST Framework Standards

- Use Pydantic schemas for request payload validation required by the exercise.
- Use DRF serializers for ORM model input/output where they reduce duplicate mapping.
- Use `serializer.is_valid(raise_exception=True)`.
- Use `ModelSerializer` for ORM-backed models.
- Set `read_only_fields` for IDs, timestamps, or calculated fields.
- Use `select_related()` or `prefetch_related()` when relationships are returned.
- Store migrations in source control.
- Return `201 Created` for create APIs and `404 Not Found` for missing resources.

## Django Without ORM Standards

- Do not place heavy logic inside `views.py`.
- Validate input using DRF serializers or Pydantic models.
- Put calculation, ML inference, or external-service logic in a service module.
- Set timeouts for outbound HTTP calls.
- Convert service exceptions into structured API responses.

## FastAPI Standards

- Use Pydantic `BaseModel` classes for every request body.
- Declare `response_model` on every route.
- Use `ConfigDict(extra="forbid")` for input models.
- Use `Field`, enums, `EmailStr`, `HttpUrl`, `UUID`, or custom validators when needed.
- Use dependency injection for settings and services.
- Raise `HTTPException` with appropriate status codes at API boundaries.
- Let FastAPI return `422 Unprocessable Entity` for Pydantic validation failures.

## Status Code Guide

| Scenario | Status |
| --- | ---: |
| Successful read | `200 OK` |
| Successful create | `201 Created` |
| Successful delete with no body | `204 No Content` |
| Bad client data in Django | `400 Bad Request` |
| Pydantic validation failure in FastAPI | `422 Unprocessable Entity` |
| Missing authentication | `401 Unauthorized` |
| Authenticated but not allowed | `403 Forbidden` |
| Resource not found | `404 Not Found` |
| Duplicate or state conflict | `409 Conflict` |
| Unexpected server failure | `500 Internal Server Error` |

## Error Response Shape

Use this shape for custom errors:

```json
{
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "The requested resource was not found.",
    "details": []
  }
}
```
