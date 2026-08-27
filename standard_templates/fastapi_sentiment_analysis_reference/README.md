# Sentiment Analysis API

FastAPI service for multilingual sentiment analysis using the approved
HuggingFace model `tabularisai/multilingual-sentiment-analysis`.

## Features

- `POST /v1/sentiment` for single-text sentiment inference
- `GET /health/ready` for readiness checks
- Structured request, response, and error contracts
- Privacy-safe logging with request and inference timing

## Environment

Copy `.env.example` to `.env` and adjust values as needed.

Required settings:

- `APP_ENV`
- `APP_VERSION`
- `LOG_LEVEL`
- `MODEL_NAME`
- `MODEL_TASK`
- `MAX_INPUT_CHARS`
- `MODEL_LOAD_ON_STARTUP`

## Local Setup

```bash
python -m venv .venv
. .venv/Scripts/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Recommended `.env` values for local development:

```env
APP_ENV=development
APP_VERSION=0.1.0
LOG_LEVEL=INFO
MODEL_NAME=tabularisai/multilingual-sentiment-analysis
MODEL_TASK=text-classification
MAX_INPUT_CHARS=5000
MODEL_LOAD_ON_STARTUP=true
```

## API Examples

Readiness:

```bash
curl http://localhost:8000/health/ready
```

Sentiment:

```bash
curl -X POST http://localhost:8000/v1/sentiment \
  -H "Content-Type: application/json" \
  -H "X-Request-ID: demo-001" \
  -d "{\"text\":\"This service is excellent.\",\"request_id\":\"demo-001\"}"
```

Example validation error:

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

## Docker

```bash
docker build -t sentiment-analysis-api .
docker run --rm -p 8000:8000 --env-file .env sentiment-analysis-api
```
