"""Command-line study planner tool using argparse (W3-3)."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from datetime import date
from pathlib import Path

from ..w2.io_utils import load_tasks
from ..w2.models import Task


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser for the study planner CLI."""
    parser = argparse.ArgumentParser(
        description="Plan study hours for tonight from a tasks CSV file.",
    )
    parser.add_argument(
        "csv_path",
        type=Path,
        help="Path to the CSV file containing task definitions.",
    )
    parser.add_argument(
        "--hours",
        type=float,
        default=2.0,
        help="Total study hours available tonight (default: 2.0).",
    )
    parser.add_argument(
        "--today",
        type=_parse_iso_date,
        default=None,
        help="Reference date in YYYY-MM-DD format (default: current date).",
    )
    return parser


def _parse_iso_date(value: str) -> date:
    """Validate and parse an ISO date string for argparse."""
    try:
        return date.fromisoformat(value.strip())
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            f"Invalid date format: {value!r}. Expected YYYY-MM-DD."
        ) from exc


def _priority_key(task: Task, today: date) -> tuple[int, float]:
    """Calculate prioritization score: urgency ratio (importance / days_left)."""
    days_left = task.days_left(today)
    if days_left <= 0:
        return (1, float(task.importance))
    return (0, task.importance / days_left)


def _allocate_hours(
    tasks: list[Task], hours: float, today: date
) -> list[tuple[Task, float]]:
    """Greedily allocate available hours to highest-priority tasks."""
    ordered_tasks = sorted(
        tasks, key=lambda t: _priority_key(t, today), reverse=True
    )
    plan: list[tuple[Task, float]] = []
    remaining = float(hours)

    for task in ordered_tasks:
        if remaining <= 1e-9:
            break
        if task.effort_h <= 0:
            continue

        allocated = round(min(task.effort_h, remaining), 10)
        plan.append((task, allocated))
        remaining = round(remaining - allocated, 10)

    return plan


def _print_plan(plan: list[tuple[Task, float]]) -> None:
    """Display the study schedule in aligned human-readable format."""
    total_hours = sum(h for _, h in plan)
    print(f"Tonight ({total_hours:.1f} h):")
    if not plan:
        print("  No study blocks scheduled.")
        return

    max_len = max(len(task.title) for task, _ in plan)
    for idx, (task, hours) in enumerate(plan, start=1):
        dots = "." * (max_len - len(task.title) + 6)
        print(f"  {idx}. {task.title} {dots} {hours:.1f} h")


def main(argv: Sequence[str] | None = None) -> int:
    """Execute the CLI interface."""
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.hours < 0:
        parser.error("--hours cannot be negative")

    today = args.today or date.today()
    csv_file = Path(args.csv_path)

    if not csv_file.is_file():
        print(f"Error: file not found: {csv_file}", file=sys.stderr)
        return 1

    try:
        tasks = load_tasks(csv_file)
    except (OSError, ValueError) as exc:
        print(f"Error: failed to load tasks from {csv_file}: {exc}", file=sys.stderr)
        return 1

    plan = _allocate_hours(tasks, args.hours, today)
    _print_plan(plan)
    return 0


if __name__ == "__main__":
    sys.exit(main())
