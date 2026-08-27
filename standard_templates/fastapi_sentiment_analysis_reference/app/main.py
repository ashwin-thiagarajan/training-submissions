from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api.routes.health import router as health_router
from app.api.routes.sentiment import router as sentiment_router
from app.core.config import Settings, get_settings
from app.core.exceptions import AppError
from app.core.logging import configure_logging, get_logger
from app.core.middleware import RequestContextMiddleware
from app.schemas.error import ErrorResponse
from app.services.sentiment_service import SentimentService


def create_app(
    settings: Settings | None = None,
    sentiment_service: SentimentService | None = None,
) -> FastAPI:
    resolved_settings = settings or get_settings()

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        configure_logging(resolved_settings.log_level)
        app.state.settings = resolved_settings
        app.state.sentiment_service = sentiment_service or SentimentService(
            resolved_settings
        )
        if resolved_settings.model_load_on_startup:
            try:
                app.state.sentiment_service.load_model()
            except AppError:
                # Keep the API running so readiness and error contracts still work.
                pass
        yield

    application = FastAPI(
        title="Sentiment Analysis API",
        version=resolved_settings.app_version,
        lifespan=lifespan,
    )
    application.add_middleware(RequestContextMiddleware)
    application.include_router(sentiment_router)
    application.include_router(health_router)

    @application.exception_handler(AppError)
    async def handle_app_error(request: Request, exc: AppError) -> JSONResponse:
        request_id = getattr(request.state, "request_id", "unknown")
        payload = ErrorResponse(
            request_id=request_id,
            error_code=exc.error_code,
            message=exc.message,
            details=exc.details,
            retryable=exc.retryable,
        )
        return JSONResponse(status_code=exc.status_code, content=payload.model_dump())

    @application.exception_handler(RequestValidationError)
    async def handle_validation_error(
        request: Request,
        exc: RequestValidationError,
    ) -> JSONResponse:
        request_id = getattr(request.state, "request_id", "unknown")
        details = {
            "errors": [
                {"field": ".".join(str(item) for item in err["loc"]), "reason": err["msg"]}
                for err in exc.errors()
            ]
        }
        payload = ErrorResponse(
            request_id=request_id,
            error_code="validation_error",
            message="Request validation failed.",
            details=details,
            retryable=False,
        )
        return JSONResponse(status_code=400, content=payload.model_dump())

    @application.exception_handler(Exception)
    async def handle_unexpected_error(
        request: Request,
        exc: Exception,
    ) -> JSONResponse:
        logger = get_logger("api.errors")
        logger.exception(
            "unexpected_error",
            extra={
                "operation": "unexpected_error",
                "request_id": getattr(request.state, "request_id", "unknown"),
            },
        )
        payload = ErrorResponse(
            request_id=getattr(request.state, "request_id", "unknown"),
            error_code="internal_error",
            message="Internal server error.",
            details=None,
            retryable=True,
        )
        return JSONResponse(status_code=500, content=payload.model_dump())

    return application


app = create_app()
