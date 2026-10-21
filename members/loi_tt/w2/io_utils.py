import csv
import json
from datetime import date
from .models import Task

def load_tasks(path: str) -> list[Task]:
    tasks = []
    with open(path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for line_num, row in enumerate(reader, start=2):
            try:
                task = Task(
                    title=row['title'],
                    importance=int(row['importance']),
                    effort_h=float(row['effort_h']),
                    deadline=date.fromisoformat(row['deadline'])
                )
                tasks.append(task)
            except Exception as e:
                raise ValueError(f"Error at line {line_num}: {e}")
    return tasks

def save_json(tasks: list[Task], path) -> None:
    # Convert list of Task objects into a list of dictionaries
    data = []
    for task in tasks:
        data.append({
            "title": task.title,
            "importance": task.importance,
            "effort_h": task.effort_h,
            # Convert date object to ISO string (e.g., "2026-10-30")
            "deadline": task.deadline.isoformat()
        })
    
    # Write the dictionary list to a JSON file
    with open(path, mode='w', encoding='utf-8') as file:
        json.dump(data, file, indent=2)