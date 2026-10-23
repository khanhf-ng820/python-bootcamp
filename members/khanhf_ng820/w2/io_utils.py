import csv
import json
from datetime import date
from pathlib import Path

from members.khanhf_ng820.w2.models import Task


def load_tasks(path: str | Path) -> list[Task]:
    tasks: list[Task] = []
    with open(path, mode="r", encoding="utf-8") as f:
        reader = csv.reader(f)
        try:
            next(reader)
        except StopIteration:
            return tasks

        for line_no, row in enumerate(reader, start=2):
            if len(row) != 4:
                raise ValueError(f"Invalid row format at line {line_no}")
            title, raw_importance, raw_effort, raw_deadline = row
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


def save_json(tasks: list[Task], path: str | Path) -> None:
    data = [
        {
            "title": t.title,
            "importance": t.importance,
            "effort_h": t.effort_h,
            "deadline": t.deadline.isoformat(),
        }
        for t in tasks
    ]
    with open(path, mode="w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
