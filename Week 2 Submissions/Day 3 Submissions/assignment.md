# Day 3 Assignment: FastAPI Ticket Classification API

## Submission Folder

```text
day3_fastapi_ticket_api/
```

Use this reference template for FastAPI project conventions:

```text
week2_training/standard_templates/fastapi_sentiment_analysis_reference/
```

Do not copy it blindly. Adapt the structure to the ticket classification API and apply the Week 2 quality checklist.

## Objective

Build a FastAPI service that classifies support tickets by priority.

## Endpoint

| Method | Path | Behavior |
| --- | --- | --- |
| `POST` | `/api/v1/tickets/classify` | Return ticket priority and recommended team |

## Request Fields

- `title`: required string, 5 to 120 characters.
- `description`: required string, 20 to 5000 characters.
- `customer_tier`: enum with `FREE`, `STANDARD`, `PREMIUM`, `ENTERPRISE`.
- `affected_users`: integer between 1 and 100000.
- `system_down`: boolean.

## Response Fields

- `priority`: `LOW`, `MEDIUM`, `HIGH`, or `CRITICAL`.
- `recommended_team`: `SUPPORT`, `ENGINEERING`, or `SRE`.
- `reasons`: list of strings.

## Business Rules

- If `system_down=true`, priority is `CRITICAL` and team is `SRE`.
- If affected users are greater than 1000, priority is at least `HIGH`.
- If customer tier is `ENTERPRISE`, priority is at least `HIGH`.
- Otherwise classify as `MEDIUM` for `PREMIUM`, else `LOW`.

## Requirements

- Use Pydantic models with `ConfigDict(extra="forbid")`.
- Use enums for fixed values.
- Declare `response_model`.
- Add `/health` endpoint.
- Centralize settings using `pydantic-settings`.
- Add logging.
- Add unit tests for all priority branches and validation failures.
