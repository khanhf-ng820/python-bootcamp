"""CLI entry point for kiethm07 W2 package (W2-5)."""

import sys
from pathlib import Path

from .io_utils import load_tasks


def main() -> None:
    """Load and display study tasks from a CSV file."""
    repo_root = Path(__file__).resolve().parents[3]
    default_csv = repo_root / "samples" / "tasks.csv"
    csv_path = Path(sys.argv[1]) if len(sys.argv) > 1 else default_csv

    tasks = load_tasks(csv_path)
    print(f"Loaded {len(tasks)} tasks from {csv_path.name}:")
    for task in tasks:
        print(
            f"- {task.title} (importance: {task.importance}, "
            f"effort: {task.effort_h}h, deadline: {task.deadline})"
        )


if __name__ == "__main__":
    main()
