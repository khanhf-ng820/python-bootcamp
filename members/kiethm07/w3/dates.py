"""Date parsing utilities for study planner (W3-1)."""

import re
from datetime import date, timedelta

_WEEKDAYS: dict[str, int] = {
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
    """Parse relative or absolute date expressions into a concrete date.

    Supported patterns:
        - ISO format: 'YYYY-MM-DD'
        - 'today'
        - 'tomorrow'
        - 'in N days' or 'in N day'
        - Weekday names (e.g. 'Fri', 'Tuesday') for the next upcoming occurrence.
          A weekday that matches today returns the occurrence 7 days ahead.

    Raises:
        ValueError: If text cannot be parsed into a valid date.
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

    if lowered in _WEEKDAYS:
        target_wd = _WEEKDAYS[lowered]
        days_ahead = (target_wd - today.weekday()) % 7
        return today + timedelta(days=days_ahead or 7)

    try:
        return date.fromisoformat(cleaned)
    except ValueError as exc:
        raise ValueError(f"Unknown due date expression: {text!r}") from exc
