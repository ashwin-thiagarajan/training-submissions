class AppError(Exception):
    def __init__(self, message: str, status_code: int = 400) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class TicketClassificationError(AppError):
    def __init__(self, message: str = "Ticket classification failed.") -> None:
        super().__init__(message, status_code=500)

