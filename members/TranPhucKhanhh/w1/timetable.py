"""W1 timetable grouping."""


def by_day(vec: list[tuple[str, str]]) -> dict[str, list[str]]:
    """Group course codes by day and sort the codes within each day."""
    grouped = {}

    for course in vec:
        grouped.setdefault(course[1], []).append(course[0])

    for list in grouped.values():
        list.sort()

    return grouped
