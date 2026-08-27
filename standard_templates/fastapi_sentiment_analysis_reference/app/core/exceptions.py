from typing import Any


class AppError(Exception):
    def __init__(
        self,
        message: str,
        *,
        status_code: int,
        error_code: str,
        retryable: bool = False,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.retryable = retryable
        self.details = details


class InputValidationError(AppError):
    def __init__(self, message: str, *, details: dict[str, Any] | None = None) -> None:
        super().__init__(
            message,
            status_code=400,
            error_code="validation_error",
            retryable=False,
            details=details,
        )


class ModelNotReadyError(AppError):
    def __init__(self, message: str = "Sentiment model is not ready.") -> None:
        super().__init__(
            message,
            status_code=500,
            error_code="model_not_ready",
            retryable=True,
        )


class InferenceFailedError(AppError):
    def __init__(self, message: str = "Sentiment inference failed.") -> None:
        super().__init__(
            message,
            status_code=500,
            error_code="inference_failed",
            retryable=True,
        )

