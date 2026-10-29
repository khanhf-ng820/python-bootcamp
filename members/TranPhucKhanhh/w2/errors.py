"""W2-3: Report when tasks exceed the available hours."""

from .models import Task


class InfeasiblePlan(Exception):
    """A complete plan needs more hours than are available."""

    def __init__(self, needed_h: float, available_h: float) -> None:
        """Record the requested and available study hours."""
        self.needed_h = needed_h
        self.available_h = available_h
        super().__init__(needed_h, available_h)

    def __str__(self) -> str:
        """Explain the study-time shortfall."""
        return (
            f"Plan needs {self.needed_h} hours, "
            f"but only {self.available_h} hours are available."
        )


def check_feasible(tasks: list[Task], available_h: float) -> None:
    """Raise InfeasiblePlan if completing every task exceeds the budget."""
    needed_h = sum(task.effort_h for task in tasks)
    if needed_h > available_h:
        raise InfeasiblePlan(needed_h, available_h)
