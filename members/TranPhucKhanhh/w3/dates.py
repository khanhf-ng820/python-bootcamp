"""W3-1: Parse absolute and relative due dates."""

import re
from datetime import date, timedelta

_WEEKDAYS = (
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday",
)


def parse_due(text: str, today: date) -> date:
    """Parse ISO dates, tomorrow, in N days, or a weekday's next occurrence.

    Weekday names may be full names or three-letter abbreviations. A weekday
    matching today means next week. Unknown input raises ValueError.
    """
    value = text.strip().lower()
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        return date.fromisoformat(value)
    if value == "tomorrow":
        return today + timedelta(days=1)

    relative = re.fullmatch(r"in\s+(\d+)\s+days?", value)
    if relative:
        try:
            return today + timedelta(days=int(relative.group(1)))
        except OverflowError as exc:
            raise ValueError("Due date is outside the supported date range") from exc

    for weekday, name in enumerate(_WEEKDAYS):
        if value in (name, name[:3]):
            days_ahead = (weekday - today.weekday()) % 7 or 7
            return today + timedelta(days=days_ahead)

    raise ValueError(f"Unknown due date: {text!r}")
