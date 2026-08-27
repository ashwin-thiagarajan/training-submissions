from dataclasses import dataclass

from app.core.exceptions import InputValidationError


@dataclass(slots=True)
class NormalizedText:
    text: str
    input_size: int


def normalize_text(text: str, max_input_chars: int) -> NormalizedText:
    normalized = text.strip()
    if not normalized:
        raise InputValidationError(
            "Text must not be empty.",
            details={"field": "text", "reason": "empty"},
        )
    if len(normalized) > max_input_chars:
        raise InputValidationError(
            f"Text must not exceed {max_input_chars} characters.",
            details={"field": "text", "reason": "too_long"},
        )
    if "\x00" in normalized:
        raise InputValidationError(
            "Text contains unsupported content.",
            details={"field": "text", "reason": "unsupported_content"},
        )
    return NormalizedText(text=normalized, input_size=len(normalized))

