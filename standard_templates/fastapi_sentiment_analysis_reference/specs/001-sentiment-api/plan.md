# Implementation Plan: Sentiment Analysis API

**Branch**: `001-sentiment-api` | **Date**: 2026-03-15 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-sentiment-api/spec.md`

**Note**: This plan is generated manually in the local repository root because
the bundled Speckit scripts resolve the parent git root instead of the current
folder. Artifact structure and content follow the repository constitution and
the Speckit planning template.

## Summary

Build a FastAPI web service that accepts a single text input, runs sentiment
classification with the approved HuggingFace model
`tabularisai/multilingual-sentiment-analysis`, returns a typed sentiment result,
and exposes structured validation, readiness, logging, timing, and error
behavior required for production use.

## Technical Context

**Language/Version**: Python 3.11  
**Primary Dependencies**: FastAPI, Pydantic v2, transformers, torch, uvicorn  
**Storage**: N/A  
**Testing**: pytest  
**Target Platform**: Linux server container runtime  
**Project Type**: web-service  
**Performance Goals**: 95% of valid requests complete within 3 seconds under
normal operating conditions  
**Constraints**: Single-text synchronous inference API; multilingual input
support; privacy-safe logging with no raw text retention by default; structured
4xx/5xx responses; request and inference timing required  
**Scale/Scope**: Initial release supports one text item per request, a single
approved model, readiness reporting, and API documentation for pilot
integrators

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- Pass: FastAPI structure keeps route handlers thin and assigns business logic
  to `app/services/sentiment_service.py`.
- Pass: API request, response, validation, and error contract changes are
  documented in the spec and captured in `contracts/openapi.yaml`.
- Pass: Model behavior remains anchored to
  `tabularisai/multilingual-sentiment-analysis` with explicit governance for any
  future label, confidence, or preprocessing changes.
- Pass: Multilingual input assumptions, payload limits, and failure modes are
  documented in the spec, research, quickstart, and contract artifacts.
- Pass: Verification strategy covers endpoint behavior, business logic,
  validation failures, readiness behavior, and observable integration behavior.
- Pass: Observability includes structured logging, request timing, inference
  timing, and privacy-safe handling of submitted text.
- Pass: Deployment impact covers `.env`, `requirements.txt`, `Dockerfile`, and
  README/runtime documentation updates required for release.
- Pass: Added complexity beyond a simple synchronous inference API is limited to
  model lifecycle management, centralized error handling, and timing middleware,
  all of which are required by the constitution.

## Project Structure

### Documentation (this feature)

```text
specs/001-sentiment-api/
|-- plan.md
|-- research.md
|-- data-model.md
|-- quickstart.md
|-- contracts/
|   `-- openapi.yaml
`-- tasks.md
```

### Source Code (repository root)

```text
app/
|-- api/
|   |-- routes/
|   |   |-- health.py
|   |   `-- sentiment.py
|   `-- dependencies.py
|-- core/
|   |-- config.py
|   |-- exceptions.py
|   |-- logging.py
|   `-- middleware.py
|-- models/
|   `-- sentiment.py
|-- schemas/
|   |-- error.py
|   |-- health.py
|   `-- sentiment.py
|-- services/
|   `-- sentiment_service.py
|-- utils/
|   `-- text_normalization.py
`-- main.py

tests/
|-- contract/
|   `-- test_sentiment_contract.py
|-- integration/
|   |-- test_health_endpoint.py
|   `-- test_sentiment_endpoint.py
`-- unit/
    |-- test_sentiment_service.py
    `-- test_text_normalization.py
```

**Structure Decision**: Use a single FastAPI service organized under `app/`
with dedicated route, schema, service, and core modules. This satisfies the
constitution requirement for modular architecture while keeping the project
simple for a synchronous inference API.

## Phase 0: Research Summary

- Model lifecycle: load the approved model once during application startup and
  reuse it across requests to avoid repeated initialization cost.
- Validation boundary: enforce single-text payloads with explicit size limits
  and whitespace rejection at the API contract boundary.
- Output contract: expose a stable sentiment label, confidence score, model
  metadata, and request correlation information without leaking internal model
  details that may change.
- Error strategy: centralize validation, domain, and infrastructure errors into
  structured 4xx/5xx responses with no stack traces in client responses.
- Observability: implement request-timing middleware plus service-level timing
  logs for preprocessing, inference, and post-processing.

## Phase 1: Design Summary

- Data model artifacts define request, result, readiness, and error objects with
  validation rules and lifecycle expectations.
- Contract artifacts define two public endpoints: `/v1/sentiment` for inference
  and `/health/ready` for readiness checks.
- Quickstart documents local setup, environment variables, startup, and example
  requests so integrators can validate the feature end to end.
- Local agent context is updated in `AGENTS.md` to capture the active
  technologies and project structure for subsequent implementation work.

## Post-Design Constitution Check

- Pass: Phase 1 artifacts preserve thin routes, typed contracts, centralized
  error handling, model governance, and privacy-safe observability.
- Pass: The design remains a single synchronous inference API with no unjustified
  persistence, queueing, or external orchestration complexity.
- Pass: Documentation and test scope explicitly cover validation, readiness,
  structured errors, and timing behavior required by the constitution.

## Complexity Tracking

No constitution violations or exception requests were identified. This feature
stays within the expected complexity envelope for a production FastAPI service.
