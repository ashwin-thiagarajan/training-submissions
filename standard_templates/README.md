# Standard Reference Templates

These folders are reference implementations learners can inspect for code organization and project conventions.

## Django Reference

```text
week2_training/standard_templates/django_qtx_reference/
```

Source:

```text
/Users/ravikanth.boggavarapu/Library/CloudStorage/OneDrive-QuadraticInsightsPvtLtd/Projects/Q Arch Team/DjangoAPP/q-django-api.zip
```

Use this to understand:

- Django project/app structure.
- Environment file usage.
- Config file usage.
- Middleware and request logging patterns.
- DRF `APIView` structure.
- Pydantic request validation pattern.
- Docker and requirements file placement.

Important: Treat this as a reference template. Learners should still apply the Week 2 quality checklist, especially around status codes, structured errors, no `print()`, and specific exception handling.

## FastAPI Reference

```text
week2_training/standard_templates/fastapi_sentiment_analysis_reference/
```

Source:

```text
/Users/ravikanth.boggavarapu/Library/CloudStorage/OneDrive-QuadraticInsightsPvtLtd/Projects/Q Arch Team/Speckit/sentiment-analysis
```

Use this to understand:

- `app/core`, `app/api/routes`, `app/schemas`, `app/services` folder structure.
- Pydantic settings with `.env`.
- Centralized logging.
- Custom exception classes and handlers.
- Request/response schemas.
- Unit, contract, and integration test organization.
- Docker and OpenAPI/spec-first documentation.

The local `.codex`, `.idea`, and other workspace/cache folders from the source project are intentionally not included.

