# Quickstart: Sentiment Analysis API

## Prerequisites

- Python 3.11
- A virtual environment tool of your choice
- Network access to download the approved HuggingFace model on first setup

## Setup

1. Create and activate a virtual environment.
2. Install dependencies from `requirements.txt`.
3. Create a `.env` file with the required configuration values:
   - `APP_ENV=development`
   - `APP_VERSION=0.1.0`
   - `MODEL_TASK=text-classification`
   - `MODEL_NAME=tabularisai/multilingual-sentiment-analysis`
   - `MAX_INPUT_CHARS=5000`
   - `LOG_LEVEL=INFO`
   - `MODEL_LOAD_ON_STARTUP=true`
4. Start the API server with the project's FastAPI entry point.

## Verify Readiness

Send a readiness request:

```bash
curl -X GET http://localhost:8000/health/ready
```

Expected response when ready:

```json
{
  "status": "ready",
  "model_loaded": true,
  "version": "0.1.0",
  "checked_at": "2026-03-15T00:00:00Z"
}
```

## Submit a Sentiment Request

```bash
curl -X POST http://localhost:8000/v1/sentiment \
  -H "Content-Type: application/json" \
  -H "X-Request-ID: demo-001" \
  -d '{
    "text": "This multilingual sentiment API is excellent.",
    "request_id": "demo-001"
  }'
```

Expected success response:

```json
{
  "request_id": "demo-001",
  "label": "positive",
  "confidence": 0.98,
  "model_name": "tabularisai/multilingual-sentiment-analysis",
  "input_size": 44,
  "processed_at": "2026-03-15T00:00:00Z"
}
```

## Validation Failure Example

```bash
curl -X POST http://localhost:8000/v1/sentiment \
  -H "Content-Type: application/json" \
  -d '{"text": ""}'
```

Expected failure response:

```json
{
  "request_id": "demo-001",
  "error_code": "validation_error",
  "message": "Request validation failed.",
  "details": {
    "errors": [
      {
        "field": "body.text",
        "reason": "Value error, Text must not be empty."
      }
    ]
  },
  "retryable": false
}
```

## Model-Not-Ready Failure Example

If the model has not been loaded yet or startup loading is disabled, the API
returns a structured `500` response:

```json
{
  "request_id": "demo-001",
  "error_code": "model_not_ready",
  "message": "Sentiment model is not ready.",
  "details": null,
  "retryable": true
}
```

## Verification Scope

- Readiness responds with `200` when the model is loaded.
- Sentiment requests return a structured `200` response with label and
  confidence.
- Invalid requests return structured `400` responses.
- Requests with unsupported or unprocessable content are rejected as `400`
  validation errors.
- Unexpected model or runtime failures return structured `500` responses without
  raw stack traces.
- Logs contain request and inference timing without storing raw text by default.
