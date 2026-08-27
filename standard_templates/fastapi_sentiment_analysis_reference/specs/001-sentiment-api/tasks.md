# Tasks: Sentiment Analysis API

**Input**: Design documents from `/specs/001-sentiment-api/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Story verification is MANDATORY. Automated tests are REQUIRED for
endpoint behavior, business logic, validation failures, and other observable
changes unless the plan documents a narrowly scoped exception.

**Organization**: Tasks are grouped by user story to enable independent
implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `app/`, `tests/` at repository root
- Paths below follow the implementation plan structure for this FastAPI service

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and base repository structure

- [ ] T001 Create the FastAPI project directory structure in `app/`, `tests/`, and `configs/` according to `specs/001-sentiment-api/plan.md`
- [ ] T002 Create dependency and environment bootstrap files in `requirements.txt`, `.env.example`, and `.gitignore`
- [ ] T003 [P] Create application entrypoint and package markers in `app/main.py`, `app/__init__.py`, `app/api/__init__.py`, `app/api/routes/__init__.py`, `app/core/__init__.py`, `app/models/__init__.py`, `app/schemas/__init__.py`, `app/services/__init__.py`, and `app/utils/__init__.py`
- [ ] T004 [P] Configure test discovery and shared fixtures in `pytest.ini` and `tests/conftest.py`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**CRITICAL**: No user story work can begin until this phase is complete

- [ ] T005 Implement settings management and typed environment loading in `app/core/config.py`
- [ ] T006 [P] Define shared domain models and runtime state objects in `app/models/sentiment.py`
- [ ] T007 [P] Define shared Pydantic schemas in `app/schemas/sentiment.py`, `app/schemas/error.py`, and `app/schemas/health.py`
- [ ] T008 Implement centralized exceptions and error mapping in `app/core/exceptions.py`
- [ ] T009 Implement structured logging configuration in `app/core/logging.py`
- [ ] T010 Implement request-timing and correlation-id middleware in `app/core/middleware.py`
- [ ] T011 Implement text normalization helpers for trimming and size checks in `app/utils/text_normalization.py`
- [ ] T012 Implement API router composition and application startup wiring in `app/main.py` and `app/api/dependencies.py`
- [ ] T013 Record release-aligned runtime defaults and model configuration in `.env.example`, `configs/logging.yaml`, and `README.md`

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Classify Submitted Text (Priority: P1)

**Goal**: Deliver a working sentiment inference API for valid single-text requests

**Independent Test**: Submit valid multilingual text to `POST /v1/sentiment`
and confirm a `200` response with sentiment label, confidence, model name, and
request correlation data.

### Verification for User Story 1

> **NOTE: Every story needs an independent verification path before merge.**

- [ ] T014 [P] [US1] Define the US1 verification workflow and sample requests in `specs/001-sentiment-api/quickstart.md`

### Tests for User Story 1

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T015 [P] [US1] Add contract tests for `POST /v1/sentiment` success responses in `tests/contract/test_sentiment_contract.py`
- [ ] T016 [P] [US1] Add integration tests for valid sentiment requests in `tests/integration/test_sentiment_endpoint.py`
- [ ] T017 [P] [US1] Add unit tests for text normalization and label mapping in `tests/unit/test_text_normalization.py` and `tests/unit/test_sentiment_service.py`

### Implementation for User Story 1

- [ ] T018 [US1] Implement model loading, inference orchestration, and label normalization in `app/services/sentiment_service.py`
- [ ] T019 [US1] Implement the sentiment request/response route in `app/api/routes/sentiment.py`
- [ ] T020 [US1] Integrate startup model initialization and service dependency wiring in `app/main.py` and `app/api/dependencies.py`
- [ ] T021 [US1] Add privacy-safe inference timing and success logging in `app/services/sentiment_service.py` and `app/core/middleware.py`

**Checkpoint**: User Story 1 should now be fully functional and testable independently

---

## Phase 4: User Story 2 - Receive Clear Failure Feedback (Priority: P2)

**Goal**: Deliver structured validation and failure behavior for invalid or failed sentiment requests

**Independent Test**: Submit empty, malformed, oversized, and simulated
service-failure requests to `POST /v1/sentiment` and confirm documented `400`
or `500` responses with stable error payloads and no stack traces.

### Verification for User Story 2

- [ ] T022 [P] [US2] Define the US2 failure verification scenarios in `specs/001-sentiment-api/quickstart.md`

### Tests for User Story 2

- [ ] T023 [P] [US2] Add contract tests for `400` and `500` error responses in `tests/contract/test_sentiment_contract.py`
- [ ] T024 [P] [US2] Add integration tests for invalid and failure-path sentiment requests in `tests/integration/test_sentiment_endpoint.py`
- [ ] T025 [P] [US2] Add unit tests for exception mapping and retryability flags in `tests/unit/test_sentiment_service.py`

### Implementation for User Story 2

- [ ] T026 [US2] Enforce empty, whitespace, unknown-field, and oversize validation rules in `app/schemas/sentiment.py` and `app/utils/text_normalization.py`
- [ ] T027 [US2] Implement model-not-ready and inference-failed domain exceptions in `app/core/exceptions.py` and `app/services/sentiment_service.py`
- [ ] T028 [US2] Return structured error responses from `app/api/routes/sentiment.py` through centralized handlers in `app/main.py`
- [ ] T029 [US2] Add failure logging without raw-text retention in `app/core/logging.py`, `app/core/middleware.py`, and `app/services/sentiment_service.py`

**Checkpoint**: User Stories 1 and 2 should both work independently

---

## Phase 5: User Story 3 - Trust Service Readiness and Usage Boundaries (Priority: P3)

**Goal**: Deliver readiness reporting and usage documentation that make service adoption safe and predictable

**Independent Test**: Call `GET /health/ready`, inspect the published API
contract and quickstart, and confirm a stakeholder can determine readiness,
input boundaries, and expected response shapes.

### Verification for User Story 3

- [ ] T030 [P] [US3] Define readiness and documentation verification steps in `specs/001-sentiment-api/quickstart.md`

### Tests for User Story 3

- [ ] T031 [P] [US3] Add contract tests for `GET /health/ready` in `tests/contract/test_sentiment_contract.py`
- [ ] T032 [P] [US3] Add integration tests for ready and not-ready service states in `tests/integration/test_health_endpoint.py`
- [ ] T033 [P] [US3] Add unit tests for readiness-state evaluation in `tests/unit/test_sentiment_service.py`

### Implementation for User Story 3

- [ ] T034 [US3] Implement readiness status evaluation in `app/services/sentiment_service.py` and `app/models/sentiment.py`
- [ ] T035 [US3] Implement the readiness route in `app/api/routes/health.py`
- [ ] T036 [US3] Publish the finalized service contract and examples in `specs/001-sentiment-api/contracts/openapi.yaml`, `specs/001-sentiment-api/quickstart.md`, and `README.md`
- [ ] T037 [US3] Ensure readiness logging and degraded-state behavior are wired in `app/main.py`, `app/api/dependencies.py`, and `app/core/middleware.py`

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T038 [P] Add final documentation for setup, endpoint usage, and Docker workflow in `README.md`
- [ ] T039 Create the production container definition in `Dockerfile`
- [ ] T040 [P] Finalize release-ready dependency and environment files in `requirements.txt` and `.env.example`
- [ ] T041 Run and fix the full automated test suite in `tests/`
- [ ] T042 Validate quickstart steps against a local run and update `specs/001-sentiment-api/quickstart.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - blocks all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational completion
- **User Story 2 (Phase 4)**: Depends on Foundational completion and reuses the
  sentiment endpoint introduced in User Story 1
- **User Story 3 (Phase 5)**: Depends on Foundational completion and can be
  implemented in parallel with User Story 2 once shared runtime state exists
- **Polish (Phase 6)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: First MVP slice; no dependency on later stories
- **User Story 2 (P2)**: Builds on the sentiment route and service created for
  User Story 1 but remains independently testable through failure scenarios
- **User Story 3 (P3)**: Shares runtime state and model lifecycle pieces from
  the foundation phase; does not require User Story 2 to be complete

### Within Each User Story

- Verification criteria MUST be defined before implementation
- Tests MUST be written and fail before implementation
- Shared schemas or models before service logic
- Service logic before route wiring
- Route wiring before final observability and documentation updates

### Parallel Opportunities

- `T003` and `T004` can run in parallel after initial repository setup
- `T006` and `T007` can run in parallel after configuration scaffolding exists
- `T015`, `T016`, and `T017` can run in parallel for User Story 1
- `T023`, `T024`, and `T025` can run in parallel for User Story 2
- `T031`, `T032`, and `T033` can run in parallel for User Story 3
- `T038` and `T040` can run in parallel during the polish phase

---

## Parallel Example: User Story 1

```bash
# Launch the US1 verification tasks together:
Task: "Add contract tests for POST /v1/sentiment success responses in tests/contract/test_sentiment_contract.py"
Task: "Add integration tests for valid sentiment requests in tests/integration/test_sentiment_endpoint.py"
Task: "Add unit tests for text normalization and label mapping in tests/unit/test_text_normalization.py and tests/unit/test_sentiment_service.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1
4. Stop and validate `POST /v1/sentiment` end to end

### Incremental Delivery

1. Deliver Setup + Foundational to establish the service skeleton
2. Deliver User Story 1 as the first usable sentiment inference API
3. Add User Story 2 to harden validation and failure behavior
4. Add User Story 3 to publish readiness and usage boundaries
5. Finish with Phase 6 for release readiness artifacts

### Parallel Team Strategy

1. One engineer completes Phase 1 and Phase 2
2. After the foundation is stable:
   - Engineer A can finish User Story 1
   - Engineer B can prepare User Story 2 tests and error contracts
   - Engineer C can prepare User Story 3 readiness tests and docs
3. Merge story slices independently after each checkpoint passes

---

## Notes

- [P] tasks affect different files and can proceed in parallel
- Each user story phase has explicit independent verification criteria
- Every task includes an exact file path for direct execution by an LLM or developer
- Suggested MVP scope: Phase 1, Phase 2, and Phase 3 only
