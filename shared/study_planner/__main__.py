"""Command-line interface for the shared Study Planner (Team T-W3)."""

import argparse
import sys
from datetime import date
from pathlib import Path

from shared.study_planner.allocate import allocate
from shared.study_planner.parse import parse_csv
from shared.study_planner.prioritise import prioritise
from shared.study_planner.render import render
from shared.study_planner.summary import summarise


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line argument parser for the study planner."""
    parser = argparse.ArgumentParser(
        description="Plan and allocate study time from a task CSV."
    )
    parser.add_argument(
        "csv_path",
        type=Path,
        help="Path to tasks CSV file.",
    )
    parser.add_argument(
        "--hours",
        type=float,
        required=True,
        help="Total available study hours (must be non-negative).",
    )
    parser.add_argument(
        "--today",
        type=str,
        default=None,
        help="Reference date in YYYY-MM-DD format (defaults to current date).",
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Include summary statistics in the output plan.",
    )
    return parser


def main(argv: list[str] | None = None) -> None:
    """Execute the study planner pipeline."""
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.hours < 0:
        parser.error("Hours cannot be negative")

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
        tasks = parse_csv(args.csv_path)
    except (ValueError, OSError) as exc:
        sys.stderr.write(f"Error: Failed to parse CSV '{args.csv_path}': {exc}\n")
        sys.exit(1)

    if not tasks:
        sys.stderr.write(f"Error: CSV file '{args.csv_path}' contains no tasks.\n")
        sys.exit(1)

    prioritized = prioritise(tasks, today)
    blocks = allocate(prioritized, args.hours)
    summary_data = summarise(tasks, blocks) if args.summary else None
    output = render(blocks, summary_data)
    print(output)


if __name__ == "__main__":
    main()
