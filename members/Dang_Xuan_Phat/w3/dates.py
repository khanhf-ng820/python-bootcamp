"""Parse flexible due-date expressions into concrete dates (W3-1)."""

from __future__ import annotations

import re
from datetime import date, timedelta

_WEEKDAY_MAP: dict[str, int] = {
    "mon": 0,
    "monday": 0,
    "tue": 1,
    "tuesday": 1,
    "wed": 2,
    "wednesday": 2,
    "thu": 3,
    "thursday": 3,
    "fri": 4,
    "friday": 4,
    "sat": 5,
    "saturday": 5,
    "sun": 6,
    "sunday": 6,
}

_IN_DAYS_PATTERN = re.compile(r"^in\s+(\d+)\s+days?$", re.IGNORECASE)


def parse_due(text: str, today: date) -> date:
    """Parse a flexible due date text relative to a given reference date.

    Supports:
    - ISO formatted dates: "YYYY-MM-DD" (e.g. "2026-10-30")
    - Relative expressions: "today", "tomorrow", "in N days"
    - Weekday names: "Mon", "Monday", "Tue", etc. (next occurrence, not today)

    Args:
        text: Input text representing the deadline.
        today: Reference date used for relative date calculations.

    Returns:
        The resolved concrete date.

    Raises:
        ValueError: If the text is empty or cannot be parsed into a valid date.
    """
    cleaned = text.strip()
    if not cleaned:
        raise ValueError("Due date string cannot be empty")

    lowered = cleaned.lower()

    if lowered == "today":
        return today

    if lowered == "tomorrow":
        return today + timedelta(days=1)

    match = _IN_DAYS_PATTERN.match(lowered)
    if match:
        days = int(match.group(1))
        return today + timedelta(days=days)

    if lowered in _WEEKDAY_MAP:
        target_weekday = _WEEKDAY_MAP[lowered]
        days_ahead = (target_weekday - today.weekday()) % 7
        return today + timedelta(days=days_ahead or 7)

    try:
        return date.fromisoformat(cleaned)
    except ValueError as exc:
        raise ValueError(f"Unknown due date expression: {text!r}") from exc
