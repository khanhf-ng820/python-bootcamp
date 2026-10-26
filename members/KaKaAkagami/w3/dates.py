"""Utilities for parsing task deadlines."""

from datetime import date, timedelta

WEEKDAYS = {
    "mon": 0,
    "tue": 1,
    "wed": 2,
    "thu": 3,
    "fri": 4,
    "sat": 5,
    "sun": 6,
}


def parse_due(text: str, today: date) -> date:
    """Parse a deadline relative to the supplied date."""
    value = text.strip().lower()

    if value == "tomorrow":
        return today + timedelta(days=1)

    if value.startswith("in ") and value.endswith(" days"):
        number = value[3:-5].strip()

        if number.isdigit():
            return today + timedelta(days=int(number))

        raise ValueError(f"Invalid deadline: {text}")

    if value in WEEKDAYS:
        days = (WEEKDAYS[value] - today.weekday()) % 7

        if days == 0:
            days = 7

        return today + timedelta(days=days)

    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"Invalid deadline: {text}") from exc