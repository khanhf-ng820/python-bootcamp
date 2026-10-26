"""Plan one evening of study from a tasks CSV file (W3-3)."""

import argparse
import sys
from collections.abc import Sequence
from datetime import date
from pathlib import Path

from ..w2.io_utils import load_tasks
from ..w2.models import Task


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="Plan one evening of study from a tasks CSV file."
    )
    parser.add_argument("csv_path", type=Path, help="CSV file with the tasks")
    parser.add_argument(
        "--hours",
        type=float,
        default=2.0,
        help="study hours available tonight (default: 2)",
    )
    parser.add_argument(
        "--today",
        type=_iso_date,
        default=None,
        help="reference date in YYYY-MM-DD form (default: today)",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the planner and return a process exit code."""
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.hours < 0:
        parser.error("--hours must be non-negative")

    today = args.today or date.today()

    try:
        tasks = load_tasks(args.csv_path)
    except (OSError, ValueError) as exc:
        print(f"Error: cannot read {args.csv_path}: {exc}", file=sys.stderr)
        return 1

    plan = _make_plan(tasks, args.hours, today)
    if not plan:
        print("No study blocks scheduled.")
        return 0

    _print_plan(plan)
    return 0


def _iso_date(value: str) -> date:
    """Parse an ISO date for argparse, raising ``ArgumentTypeError``."""
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            f"invalid date {value!r}; expected YYYY-MM-DD"
        ) from exc


def _priority(task: Task, today: date) -> tuple[int, float]:
    """Rank overdue and soon-due tasks above later ones."""
    days_left = task.days_left(today)
    if days_left <= 0:
        return (1, float(task.importance))
    return (0, task.importance / days_left)


def _make_plan(
    tasks: list[Task], hours: float, today: date
) -> list[tuple[Task, float]]:
    """Greedily assign ``hours`` to tasks in priority order."""
    ordered = sorted(tasks, key=lambda task: _priority(task, today), reverse=True)
    plan: list[tuple[Task, float]] = []
    remaining_hours = float(hours)

    for task in ordered:
        if remaining_hours <= 1e-9:
            break
        if task.effort_h <= 0:
            continue

        allocated = round(min(task.effort_h, remaining_hours), 10)
        plan.append((task, allocated))
        remaining_hours = round(remaining_hours - allocated, 10)

    return plan


def _print_plan(plan: list[tuple[Task, float]]) -> None:
    """Print the plan in a readable, aligned form."""
    total_hours = sum(hours for _, hours in plan)
    print(f"Tonight ({total_hours:.1f} h):")

    width = max(len(task.title) for task, _ in plan)
    for index, (task, hours) in enumerate(plan, start=1):
        dots = "." * (width - len(task.title) + 6)
        print(f"  {index}. {task.title} {dots} {hours:.1f} h")


if __name__ == "__main__":
    sys.exit(main())
