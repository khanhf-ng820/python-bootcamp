"""Focused tests for Tran Phuc Khanh's individual Week 3 exercises."""

from datetime import date

import pytest

from .dates import parse_due

TODAY = date(2026, 10, 6)


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("2026-10-30", date(2026, 10, 30)),
        ("2028-02-29", date(2028, 2, 29)),
        ("tomorrow", date(2026, 10, 7)),
        ("in 3 days", date(2026, 10, 9)),
        ("in 0 days", TODAY),
        ("in 1 day", date(2026, 10, 7)),
        ("Fri", date(2026, 10, 9)),
        ("Tuesday", date(2026, 10, 13)),
        (" Mon ", date(2026, 10, 12)),
    ],
)
def test_parse_due_formats(text: str, expected: date) -> None:
    """Resolve each supported date format from a supplied reference date."""
    assert parse_due(text, TODAY) == expected


@pytest.mark.parametrize(
    "text", ["someday", "", "2026-02-30", "in -3 days", "Friyay", "20261030"]
)
def test_parse_due_rejects_invalid_text(text: str) -> None:
    """Reject unknown or invalid date expressions."""
    with pytest.raises(ValueError):
        parse_due(text, TODAY)


def test_tomorrow_crosses_year_boundary() -> None:
    """Use date arithmetic correctly across the end of a year."""
    assert parse_due("tomorrow", date(2026, 12, 31)) == date(2027, 1, 1)
