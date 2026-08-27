import pytest

from app.core.exceptions import InputValidationError
from app.utils.text_normalization import normalize_text


def test_normalize_text_strips_and_counts() -> None:
    normalized = normalize_text("  hello  ", 5000)

    assert normalized.text == "hello"
    assert normalized.input_size == 5


def test_normalize_text_rejects_empty_values() -> None:
    with pytest.raises(InputValidationError):
        normalize_text("   ", 5000)


def test_normalize_text_rejects_oversized_values() -> None:
    with pytest.raises(InputValidationError):
        normalize_text("x" * 5001, 5000)


def test_normalize_text_rejects_unsupported_content() -> None:
    with pytest.raises(InputValidationError):
        normalize_text("hello\x00world", 5000)
