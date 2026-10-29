"""Study planner command-line interface tool (W3-3)."""

import argparse
import sys
from datetime import date
from pathlib import Path

from members.kiethm07.w2.io_utils import load_tasks
from members.kiethm07.w2.models import Task


def _urgency_key(task: Task, ref_date: date) -> tuple[int, float]:
    """Calculate sorting key based on urgency and importance.

    Overdue or due-today tasks receive top precedence; upcoming tasks are
    ranked by importance divided by days remaining.
    """
    days = task.days_left(ref_date)
    if days <= 0:
        return (1, float(task.importance))
    return (0, task.importance / days)


def build_schedule(
    tasks: list[Task], hours: float, ref_date: date
) -> list[tuple[str, float]]:
    """Prioritize tasks and greedily allocate available study hours.

    Args:
        tasks: List of parsed task objects.
        hours: Total available study hours.
        ref_date: Baseline date for urgency calculations.

    Returns:
        List of tuples containing (task_title, allocated_hours).
    """
    if hours <= 0:
        return []

    sorted_tasks = sorted(tasks, key=lambda t: _urgency_key(t, ref_date), reverse=True)
    allocated: list[tuple[str, float]] = []
    remaining = float(hours)

    for task in sorted_tasks:
        if remaining <= 1e-9:
            break
        if task.effort_h <= 0:
            continue
        alloc_h = min(task.effort_h, remaining)
        allocated.append((task.title, alloc_h))
        remaining = round(remaining - alloc_h, 10)

    return allocated


def format_schedule(allocated: list[tuple[str, float]], hours: float) -> str:
    """Format scheduled task allocations into a dot-leader schedule string."""
    lines = [f"Tonight ({hours:.1f} h):"]
    if not allocated:
        lines.append("  No tasks scheduled.")
        return "\n".join(lines)

    max_len = max((len(title) for title, _ in allocated), default=10)
    width = max(16, max_len + 4)

    for idx, (title, alloc_h) in enumerate(allocated, start=1):
        dot_count = max(3, width - len(title))
        lines.append(f"  {idx}. {title} {'.' * dot_count} {alloc_h:.1f} h")

    return "\n".join(lines)


def main(argv: list[str] | None = None) -> None:
    """CLI entry point for the study planner."""
    parser = argparse.ArgumentParser(
        description="Study planner command-line scheduler."
    )
    parser.add_argument("csv_path", type=Path, help="Path to input tasks CSV file.")
    parser.add_argument(
        "--hours", type=float, required=True, help="Total study hours available."
    )
    parser.add_argument(
        "--today",
        type=str,
        default=None,
        help="Reference date YYYY-MM-DD (defaults to today).",
    )

    args = parser.parse_args(argv)

    if not args.csv_path.exists():
        sys.stderr.write(f"Error: File not found: {args.csv_path}\n")
        sys.exit(1)

    if args.hours < 0:
        sys.stderr.write(
            f"Error: Study hours must be non-negative, got: {args.hours}\n"
        )
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
