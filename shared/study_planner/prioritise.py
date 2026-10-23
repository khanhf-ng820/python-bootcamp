"""Priority ranking for study tasks (Team T-W2)."""

from collections.abc import Iterable
from datetime import date

from shared.contract import Task


def _score(task: Task, today: date) -> tuple[int, float]:
    """Return a sort key for ``task``.

    The score is ``importance / days_left``. Tasks due today or already
    overdue have no positive number of days left, so they are ranked first
    and ordered among themselves by importance.
    """
    days_left = task.days_left(today)
    if days_left <= 0:
        return (1, float(task.importance))
    return (0, task.importance / days_left)


def prioritise(tasks: Iterable[Task], today: date) -> list[Task]:
    """Return ``tasks`` ordered from highest to lowest priority.

    Priority is ``importance / days_left``: important tasks with close
    deadlines come first. The input is not modified, and tasks with the same
    score keep their original order.
    """
    return sorted(tasks, key=lambda task: _score(task, today), reverse=True)
