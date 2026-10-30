"""W3-3: Run a reproducible study planner using the individual W2 loader."""

import argparse
import math
import sys
from datetime import date

from ..w2.io_utils import load_tasks


def main(argv: list[str] | None = None) -> int:
    """Print a greedy study plan; report input file errors with exit code 1."""
    parser = argparse.ArgumentParser(description="Plan tonight's study time.")
    parser.add_argument("csv_path", help="CSV file containing study tasks")
    parser.add_argument("--hours", type=float, required=True, help="Available hours")
    parser.add_argument(
        "--today",
        type=date.fromisoformat,
        default=date.today(),
        help="Reference date in YYYY-MM-DD format (default: today)",
    )
    args = parser.parse_args(argv)
    if not math.isfinite(args.hours) or args.hours < 0:
        parser.error("--hours must be a finite, non-negative number")

    try:
        tasks = load_tasks(args.csv_path)
    except (OSError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    ordered = sorted(
        tasks,
        key=lambda task: task.importance / max(1, task.days_left(args.today)),
        reverse=True,
    )
    remaining = args.hours
    lines = [f"Tonight ({args.hours:.1f} h):"]
    for task in ordered:
        if remaining <= 0:
            break
        allocated = min(task.effort_h, remaining)
        if allocated <= 0:
            continue
        lines.append(f"  {len(lines)}. {task.title} ...... {allocated:.1f} h")
        remaining = max(0.0, remaining - allocated)

    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
