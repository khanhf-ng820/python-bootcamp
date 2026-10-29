"""Expected input errors and the CLI error boundary for Team T-W3.

The CLI should load CSV input with load_tasks() and run its pipeline through
run_cli(). Argument parsing and pipeline construction stay in __main__.py.
"""

import csv
import sys
from collections.abc import Callable
from pathlib import Path

from shared.contract import Task
from shared.study_planner.parse import parse_csv


class InfeasiblePlan(Exception):
    """A caller cannot complete a plan within the available hours."""

    def __init__(self, needed_h: float, available_h: float) -> None:
        self.needed_h = needed_h
        self.available_h = available_h
        super().__init__(needed_h, available_h)

    def __str__(self) -> str:
        return (
            f"Plan needs {self.needed_h} hours, "
            f"but only {self.available_h} hours are available."
        )


def load_tasks(path: str | Path) -> list[Task]:
    """Use the shared parser, rejecting input that contains no task rows.

    File access and row-conversion errors propagate to run_cli(), which
    reports them to stderr. A header-only or blank CSV is also empty input.
    """
    tasks = parse_csv(path)
    if not tasks:
        raise ValueError(f"No tasks found in CSV file: {path}")
    return tasks


def run_cli(action: Callable[[], None]) -> int:
    """Run a CLI pipeline and return its process exit code.

    Report expected file, CSV, input, and feasibility errors without a
    traceback. Programming errors propagate for diagnosis. The caller exits
    with SystemExit(run_cli(action)); this helper does not terminate Python.

    InfeasiblePlan is handled when a caller raises it; greedy allocation of
    a partial plan remains allowed without an automatic feasibility check.
    """
    try:
        action()
    except (OSError, csv.Error, ValueError, InfeasiblePlan) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0
