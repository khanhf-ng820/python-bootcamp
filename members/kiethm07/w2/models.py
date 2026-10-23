"""Task dataclass model (W2-1)."""

from dataclasses import dataclass
from datetime import date


@dataclass
class Task:
    """Represents an individual study task with priority and deadline."""

    title: str
    importance: int
    effort_h: float
    deadline: date

    def __post_init__(self) -> None:
        if not 1 <= self.importance <= 5:
            raise ValueError("importance must be between 1 and 5")

    def days_left(self, today: date) -> int:
        """Return the number of remaining days until deadline, or 0 if past due."""
        return max(0, (self.deadline - today).days)
