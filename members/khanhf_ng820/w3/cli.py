"""Study planner CLI tool."""

import argparse
import sys
from datetime import date
from pathlib import Path

from members.khanhf_ng820.w2.io_utils import load_tasks
from members.khanhf_ng820.w2.models import Task


def _sort_key(task: Task, today: date) -> tuple[int, float]:
    """Sort key for task priority.

    Tasks due today or overdue have higher rank; upcoming tasks are ranked
    by importance / days_left.
    """
    days_left = task.days_left(today)
    if days_left <= 0:
        return (1, float(task.importance))
    return (0, task.importance / days_left)


def build_schedule(
    tasks: list[Task], hours: float, today: date
) -> list[tuple[str, float]]:
    """Prioritize and allocate available study hours across tasks."""
    if hours <= 0:
        return []

    sorted_tasks = sorted(tasks, key=lambda t: _sort_key(t, today), reverse=True)
    allocated: list[tuple[str, float]] = []
    remaining = float(hours)

    for task in sorted_tasks:
        if remaining <= 1e-9:
            break
        if task.effort_h <= 0:
            continue
        alloc = min(task.effort_h, remaining)
        allocated.append((task.title, alloc))
        remaining = round(remaining - alloc, 10)

    return allocated


def format_schedule(allocated: list[tuple[str, float]], hours: float) -> str:
    """Format allocated tasks into a dot-leader schedule string."""
    lines = [f"Tonight ({hours:.1f} h):"]
    if not allocated:
        lines.append("  No tasks scheduled.")
        return "\n".join(lines)

    max_title = max((len(title) for title, _ in allocated), default=10)
    width = max(16, max_title + 4)

    for idx, (title, alloc_h) in enumerate(allocated, start=1):
        dot_count = max(3, width - len(title))
        lines.append(f"  {idx}. {title} {'.' * dot_count} {alloc_h:.1f} h")

    return "\n".join(lines)


def main(argv: list[str] | None = None) -> None:
    """Entry point for the study planner CLI."""
    parser = argparse.ArgumentParser(description="Study planner command-line tool.")
    parser.add_argument("csv_path", type=Path, help="Path to tasks CSV file.")
    parser.add_argument(
        "--hours", type=float, required=True, help="Total available study hours."
    )
    parser.add_argument(
        "--today",
        type=str,
        default=None,
        help="Reference date YYYY-MM-DD (defaults to today).",
    )

    args = parser.parse_args(argv)

    if not args.csv_path.exists():
        sys.stderr.write(f"Error: File '{args.csv_path}' not found.\n")
        sys.exit(1)

    if args.today:
        try:
            today = date.fromisoformat(args.today)
        except ValueError:
            sys.stderr.write(
                f"Error: Invalid date format for --today: '{args.today}'. Expected YYYY-MM-DD.\n"
            )
            sys.exit(1)
    else:
        today = date.today()

    try:
        tasks = load_tasks(args.csv_path)
    except (ValueError, OSError) as exc:
        sys.stderr.write(f"Error loading tasks from '{args.csv_path}': {exc}\n")
        sys.exit(1)

    allocated = build_schedule(tasks, args.hours, today)
    print(format_schedule(allocated, args.hours))


if __name__ == "__main__":
    main()
