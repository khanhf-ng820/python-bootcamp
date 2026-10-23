"""CSV parser for study planner tasks (Team T-W2)."""

import csv
from datetime import date
from pathlib import Path

from shared.contract import Task


def parse_csv(path: str | Path) -> list[Task]:
    """Parse tasks from a CSV file.

    The CSV must have the header: title,importance,effort_h,deadline.
    Returns a list of Task objects.
    Raises ValueError with the 1-based line number on invalid rows.
    """
    tasks: list[Task] = []
    file_path = Path(path)
    with file_path.open(mode="r", encoding="utf-8") as f:
        reader = csv.reader(f)
        try:
            next(reader)
        except StopIteration:
            return tasks

        for line_no, row in enumerate(reader, start=2):
            if not row or all(not cell.strip() for cell in row):
                continue
            if len(row) != 4:
                raise ValueError(f"Invalid row format at line {line_no}")

            title, raw_importance, raw_effort, raw_deadline = [cell.strip() for cell in row]
            try:
                importance = int(raw_importance)
            except ValueError as e:
                raise ValueError(f"Invalid importance at line {line_no}") from e

            try:
                effort_h = float(raw_effort)
            except ValueError as e:
                raise ValueError(f"Invalid effort_h at line {line_no}") from e

            try:
                deadline = date.fromisoformat(raw_deadline)
            except ValueError as e:
                raise ValueError(f"Invalid deadline at line {line_no}") from e

            try:
                task = Task(title=title, importance=importance, effort_h=effort_h, deadline=deadline)
            except ValueError as e:
                raise ValueError(f"Invalid task at line {line_no}: {e}") from e

            tasks.append(task)

    return tasks
