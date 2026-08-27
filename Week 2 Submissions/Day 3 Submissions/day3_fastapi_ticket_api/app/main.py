import logging

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api.routes.health import router as health_router
from app.api.routes.tickets import router as tickets_router
from app.core.config import get_settings
from app.core.logging import configure_logging
from app.schemas.error import ErrorBody, ErrorResponse

settings = get_settings()
configure_logging(settings.log_level)
logger = logging.getLogger(__name__)

app = FastAPI(title="Ticket Classification API", version=settings.app_version)
app.include_router(tickets_router, prefix=settings.api_prefix)
app.include_router(health_router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    payload = ErrorResponse(
        error=ErrorBody(
            code="VALIDATION_ERROR",
            message="Invalid request payload.",
            details=exc.errors(),
        )
    )
    return JSONResponse(status_code=422, content=payload.model_dump())


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    payload = ErrorResponse(
        error=ErrorBody(
            code="API_ERROR",
            message=str(exc.detail),
            details=[],
        )
    )
    return JSONResponse(status_code=exc.status_code, content=payload.model_dump())


@app.exception_handler(Exception)
async def unexpected_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception("Unhandled API error")
    payload = ErrorResponse(
        error=ErrorBody(
            code="INTERNAL_ERROR",
            message="Internal server error.",
            details=[],
        )
    )
    return JSONResponse(status_code=500, content=payload.model_dump())

