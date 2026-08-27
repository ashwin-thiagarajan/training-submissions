# sentiment-analysis Development Guidelines

Auto-generated from all feature plans. Last updated: 2026-03-15

## Active Technologies

- Python 3.11 + FastAPI, Pydantic v2, transformers, torch, uvicorn (001-sentiment-api)

## Project Structure

```text
app/
tests/
specs/
```

## Commands

cd . && pytest && ruff check .

## Code Style

Python 3.11: Follow PEP8, use type hints, keep business logic out of route
handlers, and prefer typed Pydantic schemas for request and response models.

## Recent Changes

- 001-sentiment-api: Added Python 3.11 + FastAPI, Pydantic v2, transformers, torch, uvicorn

<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->
