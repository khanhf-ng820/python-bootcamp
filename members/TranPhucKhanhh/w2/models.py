"""W2-1: Task data model."""

from dataclasses import dataclass
from datetime import date


@dataclass
class Task:
    """A study task with importance, effort, and a deadline."""

    title: str
    importance: int
    effort_h: float
    deadline: date

    def __post_init__(self) -> None:
        """Validate the allowed importance range."""
        if not 1 <= self.importance <= 5:
            raise ValueError("importance must be from 1 to 5")

    def days_left(self, today: date) -> int:
        """Return the non-negative number of days until the deadline."""
        return max(0, (self.deadline - today).days)
