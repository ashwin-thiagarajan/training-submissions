# Research: Sentiment Analysis API

## Decision 1: Application Framework and Runtime

- **Decision**: Implement the service as a Python 3.11 FastAPI application
  served by Uvicorn.
- **Rationale**: This matches the organization standard, supports typed API
  contracts cleanly, and keeps middleware, exception handling, and documentation
  straightforward for a lightweight inference service.
- **Alternatives considered**:
  - Flask: rejected because it would require more custom work to match the
    organization's typed validation and documentation requirements.
  - Async task-oriented architecture: rejected because the feature scope is a
    synchronous single-text inference API and does not justify extra
    infrastructure.

## Decision 2: Model Loading Strategy

- **Decision**: Load `tabularisai/multilingual-sentiment-analysis` once during
  application startup and reuse the pipeline for subsequent requests.
- **Rationale**: Reusing a single in-memory model instance reduces repeated
  initialization cost and supports the latency objective in the specification.
- **Alternatives considered**:
  - Lazy loading on first request: rejected because it makes the first customer
    request unpredictable and complicates readiness semantics.
  - Reloading per request: rejected because it is too slow and operationally
    wasteful.

## Decision 3: Public API Shape

- **Decision**: Expose one inference endpoint for sentiment analysis and one
  readiness endpoint for operational health.
- **Rationale**: This covers the user journeys in the spec while keeping the
  public surface minimal and well bounded for an initial release.
- **Alternatives considered**:
  - Batch inference endpoint: rejected because the specification explicitly
    limits the first release to one text item per request.
  - Separate health and metadata endpoints beyond readiness: rejected because
    they are not required for the initial pilot scope.

## Decision 4: Validation Rules

- **Decision**: Reject missing, empty, whitespace-only, and oversized text
  requests at the contract boundary using typed request validation.
- **Rationale**: Early rejection keeps route and service logic simpler and gives
  API consumers precise correction feedback.
- **Alternatives considered**:
  - Silent normalization of empty text to a default value: rejected because it
    produces misleading results.
  - Allowing arbitrary payload size: rejected because it undermines predictable
    latency and resource usage.

## Decision 5: Sentiment Response Contract

- **Decision**: Return a stable response containing normalized input metadata,
  sentiment label, confidence score, model identifier, and request correlation
  information.
- **Rationale**: Consumers need a predictable business-level result while the
  implementation retains freedom to change internal transformer plumbing.
- **Alternatives considered**:
  - Returning raw model logits or all intermediate scores: rejected because it
    leaks implementation detail and complicates consumer interpretation.
  - Returning only the sentiment label: rejected because the specification
    requires confidence information.

## Decision 6: Error Handling Approach

- **Decision**: Use centralized exception mapping for validation errors, model
  availability failures, and unexpected inference errors.
- **Rationale**: This satisfies the constitution requirement for structured
  errors, correct status codes, and no raw stack traces in user responses.
- **Alternatives considered**:
  - Route-level try/except blocks: rejected because they duplicate logic and
    encourage inconsistent behavior.
  - Generic 500 responses for all failures: rejected because consumers need to
    distinguish client errors from service errors.

## Decision 7: Observability and Privacy

- **Decision**: Emit structured logs for request receipt, validation failures,
  model load status, preprocessing duration, inference duration, post-processing
  duration, and final response status without logging raw text by default.
- **Rationale**: The organization standard and constitution require both timing
  insight and privacy-safe operations.
- **Alternatives considered**:
  - Raw request-body logging: rejected because it conflicts with privacy-safe
    observability requirements.
  - Minimal logs without timings: rejected because it weakens performance
    monitoring and troubleshooting.

## Decision 8: Testing Scope

- **Decision**: Use pytest to cover contract behavior, integration behavior,
  service logic, validation failures, and representative edge cases.
- **Rationale**: This directly satisfies the organization standard and supports
  the constitution's release discipline.
- **Alternatives considered**:
  - Manual-only verification: rejected because it is insufficient for release
    quality and regression safety.
  - Unit-only testing: rejected because contract behavior is a first-class
    consumer-facing obligation.
