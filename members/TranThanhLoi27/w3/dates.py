"""Parse flexible due-date text into concrete dates (W3-1)."""

import re
from datetime import date, timedelta

_WEEKDAY_INDEX = {
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

_IN_DAYS = re.compile(r"^in\s+(\d+)\s+days?$", re.IGNORECASE)


def parse_due(text: str, today: date) -> date:
    """Parse due-date text relative to ``today``.

    Accepted forms are an ISO date (``"2026-10-30"``), ``"today"``,
    ``"tomorrow"``, ``"in N days"`` and a weekday name such as ``"Fri"``
    or ``"Friday"``. A weekday always means its next occurrence after
    ``today``, never today itself.

    Args:
        text: The due-date text to parse.
        today: The reference date for relative expressions.

    Returns:
        The resolved date.

    Raises:
        ValueError: If ``text`` is not a recognised due-date expression.
    """
    value = text.strip()
    lowered = value.lower()

    if lowered == "today":
        return today

    if lowered == "tomorrow":
        return today + timedelta(days=1)

    match = _IN_DAYS.match(lowered)
    if match:
        return today + timedelta(days=int(match.group(1)))

    if lowered in _WEEKDAY_INDEX:
        days_ahead = (_WEEKDAY_INDEX[lowered] - today.weekday()) % 7
        return today + timedelta(days=days_ahead or 7)

    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"Unknown due date: {text!r}") from exc
