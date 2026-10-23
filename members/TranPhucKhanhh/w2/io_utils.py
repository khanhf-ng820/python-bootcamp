"""W2-2: Load tasks from CSV and save them as JSON."""
import csv
import json
from datetime import date
from pathlib import Path

from .models import Task


def load_tasks(path: str | Path) -> list[Task]:
    tasks = []
    with Path(path).open(encoding="utf-8", newline="") as stream:
        reader = csv.reader(stream, strict=True)
        try:
            if next(reader, None) != ["title", "importance", "effort_h", "deadline"]:
                raise ValueError("line 1: invalid CSV header")
            for row in reader:
                try:
                    title, importance, effort_h, deadline = row
                    tasks.append(Task(
                        title, int(importance), float(effort_h),
                        date.fromisoformat(deadline),
                    ))
                except ValueError as exc:
                    raise ValueError(f"line {reader.line_num}: {exc}") from exc
        except csv.Error as exc:
            raise ValueError(f"line {max(1, reader.line_num)}: {exc}") from exc
    return tasks


def save_json(tasks: list[Task], path: str | Path) -> None:
    records = [
        {"title": task.title, "importance": task.importance,
         "effort_h": task.effort_h, "deadline": task.deadline.isoformat()}
        for task in tasks
    ]
    with Path(path).open("w", encoding="utf-8") as stream:
        json.dump(records, stream, ensure_ascii=False, indent=2)
