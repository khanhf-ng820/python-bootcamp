"""Command-line interface for Week 3 study tasks."""

import argparse
import sys
from datetime import date
from pathlib import Path

from members.KaKaAkagami.w2.io_utils import load_tasks


def main(argv: list[str] | None = None) -> int:
    """Load tasks from CSV and display the study plan."""
    parser = argparse.ArgumentParser(
        description="Week 3 Study Planner CLI"
    )
    parser.add_argument("csv_path", type=Path)
    parser.add_argument("--hours", type=float, required=True)
    parser.add_argument("--today", type=date.fromisoformat, default=date.today())

    args = parser.parse_args(argv)

    try:
        tasks = load_tasks(args.csv_path)
    except (OSError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    if args.hours < 0:
        print("Error: available hours cannot be negative", file=sys.stderr)
        return 1

    print(f"Study Planner - {args.today.isoformat()}")
    print(f"Available hours: {args.hours:g}")

    for task in tasks:
        print(
            f"- {task.title}: {task.effort_h:g}h, "
            f"importance={task.importance}, deadline={task.deadline}"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
