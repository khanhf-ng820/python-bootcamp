import csv
import json
from datetime import date
from pathlib import Path

from .models import Task


def load_tasks(path: str | Path) -> list[Task]:
    """Load tasks from a CSV file.

    Raises:
        ValueError: If a row contains invalid data, with the 1-based line number.
    """
    path = Path(path)
    tasks: list[Task] = []

    with path.open("r", encoding="utf-8") as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            return tasks

        expected_cols = ["title", "importance", "effort_h", "deadline"]
        col_indices = {col.strip(): idx for idx, col in enumerate(header)}
        for col in expected_cols:
            if col not in col_indices:
                raise ValueError(f"Missing column '{col}' in CSV header")

        for line_idx, row in enumerate(reader, start=2):
            if not row or all(not cell.strip() for cell in row):
                continue
            try:
                title = row[col_indices["title"]].strip()
                importance = int(row[col_indices["importance"]].strip())
                effort_h = float(row[col_indices["effort_h"]].strip())
                deadline = date.fromisoformat(row[col_indices["deadline"]].strip())
                task = Task(title, importance, effort_h, deadline)
                tasks.append(task)
            except Exception as exc:
                raise ValueError(f"Error parsing task at line {line_idx}: {exc}") from exc

    return tasks


def save_json(tasks: list[Task], path: str | Path) -> None:
    """Serialize tasks into a JSON file."""
    path = Path(path)
    data = [
        {
            "title": task.title,
            "importance": task.importance,
            "effort_h": task.effort_h,
            "deadline": task.deadline.isoformat(),
        }
        for task in tasks
    ]
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
