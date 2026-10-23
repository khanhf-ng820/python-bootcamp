"""Greedy allocation of available study hours into blocks (Team T-W2)."""

from collections.abc import Iterable

from shared.contract import Block, Task


def allocate(tasks: Iterable[Task], hours: float) -> list[Block]:
    """Allocate available study hours across tasks using a greedy strategy.

    Tasks are processed in the given order. Each task receives up to its
    required effort (effort_h) from the remaining available hours. Once the
    available hours are exhausted, no further blocks are allocated.

    Args:
        tasks: An iterable of Task objects to allocate hours for.
        hours: Total available study hours. Must be non-negative.

    Returns:
        A list of Block objects representing the scheduled study time.

    Raises:
        ValueError: If hours is negative or any task has negative effort_h.
    """
    if hours < 0:
        raise ValueError("Available hours cannot be negative")

    task_list = list(tasks)
    if any(task.effort_h < 0 for task in task_list):
        raise ValueError("Task effort cannot be negative")

    blocks: list[Block] = []
    remaining_hours = float(hours)

    for task in task_list:
        if remaining_hours <= 1e-9:
            break

        if task.effort_h == 0:
            continue

        allocated = min(task.effort_h, remaining_hours)
        if allocated > 0:
            blocks.append(Block(task=task, hours=allocated))
            remaining_hours = round(remaining_hours - allocated, 10)

    return blocks
