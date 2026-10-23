"""Filter tasks for the shared Study Planner."""

from datetime import date

from shared.contract import Task


def validate_tasks(tasks: list[Task], today: date) -> list[Task]:
    """Return valid tasks in input order without changing the original objects.

    Keep tasks due today or later, importance 1-5, and non-negative effort.
    """
    return [
        task
        for task in tasks
        if task.deadline >= today
        and 1 <= task.importance <= 5
        and task.effort_h >= 0
    ]
