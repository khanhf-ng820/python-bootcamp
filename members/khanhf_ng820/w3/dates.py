"""Date parsing utilities for study planner."""

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


def parse_due(text: str, today: date) -> date:
    """Parse relative or absolute date expressions into a concrete date.

    Supported patterns:
        - ISO format: 'YYYY-MM-DD'
        - 'tomorrow'
        - 'in N days' or 'in N day'
        - Weekday names (e.g. 'Fri', 'Tuesday') for the next upcoming occurrence

    Raises ValueError if text cannot be parsed.
    """
    cleaned = text.strip()
    if not cleaned:
        raise ValueError("Due date string cannot be empty")

    try:
        return date.fromisoformat(cleaned)
    except ValueError:
        pass

    lowered = cleaned.lower()

    if lowered == "tomorrow":
        return today + timedelta(days=1)

    match = re.match(r"^in\s+(\d+)\s+days?$", lowered)
    if match:
        days = int(match.group(1))
        return today + timedelta(days=days)

    if lowered in _WEEKDAYS:
        target_wd = _WEEKDAYS[lowered]
        days_ahead = (target_wd - today.weekday()) % 7
        if days_ahead == 0:
            days_ahead = 7
        return today + timedelta(days=days_ahead)

    raise ValueError(f"Unknown due date expression: {text!r}")
