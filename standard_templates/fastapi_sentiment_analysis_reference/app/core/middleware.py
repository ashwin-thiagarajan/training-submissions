import time
import uuid
from collections.abc import Awaitable, Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.logging import get_logger


class RequestContextMiddleware(BaseHTTPMiddleware):
    def __init__(self, app) -> None:  # type: ignore[no-untyped-def]
        super().__init__(app)
        self.logger = get_logger("api.middleware")

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        request.state.request_id = request_id

        started = time.perf_counter()
        self.logger.info(
            "request_received",
            extra={
                "operation": "request_received",
                "duration_ms": 0,
                "request_id": request_id,
                "path": request.url.path,
                "method": request.method,
            },
        )

        response = await call_next(request)
        duration_ms = round((time.perf_counter() - started) * 1000, 2)
        response.headers["X-Request-ID"] = request_id

        self.logger.info(
            "request_completed",
            extra={
                "operation": "request_completed",
                "duration_ms": duration_ms,
                "request_id": request_id,
                "path": request.url.path,
                "method": request.method,
                "status_code": response.status_code,
            },
        )
        return response

