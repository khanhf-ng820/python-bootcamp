from .models import Task


class InfeasiblePlan(Exception):
    """Raised when available hours are insufficient to complete scheduled tasks."""

    def __init__(self, needed_h: float, available_h: float) -> None:
        self.needed_h = needed_h
        self.available_h = available_h
        super().__init__(
            f"Infeasible plan: needed {needed_h}h, but only {available_h}h available."
        )


def check_feasible(tasks: list[Task], available_h: float) -> None:
    """Validate that tasks can be completed within available hours.

    Raises:
        InfeasiblePlan: If total effort required exceeds available hours.
    """
    needed_h = sum(task.effort_h for task in tasks)
    if needed_h > available_h:
        raise InfeasiblePlan(needed_h, available_h)
