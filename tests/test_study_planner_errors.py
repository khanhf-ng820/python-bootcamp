"""Tests for the shared Study Planner CLI error boundary."""

import csv
import subprocess
import sys
from datetime import date
from pathlib import Path

import pytest

from shared.contract import Task
from shared.study_planner.allocate import allocate
from shared.study_planner.errors import InfeasiblePlan, load_tasks, run_cli

ROOT = Path(__file__).resolve().parents[1]
HEADER = "title,importance,effort_h,deadline\n"
VALID_CSV = HEADER + "DS exam,5,6,2030-10-30\nAssignment,4,1.5,2030-10-27\n"


def test_infeasible_plan_keeps_hours_and_explains_shortfall():
    error = InfeasiblePlan(7.5, 2)

    assert error.needed_h == 7.5
    assert error.available_h == 2
    assert str(error) == "Plan needs 7.5 hours, but only 2 hours are available."


def test_load_tasks_returns_shared_tasks(tmp_path):
    path = tmp_path / "tasks.csv"
    path.write_text(VALID_CSV, encoding="utf-8")

    assert load_tasks(path) == [
        Task("DS exam", 5, 6, date(2030, 10, 30)),
        Task("Assignment", 4, 1.5, date(2030, 10, 27)),
    ]


@pytest.mark.parametrize("content", ["", "\n\n", HEADER, HEADER + "\n \n"])
def test_no_task_rows_are_rejected(tmp_path, content):
    path = tmp_path / "empty.csv"
    path.write_text(content, encoding="utf-8")

    with pytest.raises(ValueError, match="No tasks found"):
        load_tasks(path)


@pytest.mark.parametrize(
    "row",
    [
        "Exam,invalid,2,2030-10-30",
        "Exam,5,invalid,2030-10-30",
        "Exam,5,2,not-a-date",
        "Exam,5",
    ],
)
def test_invalid_rows_keep_parser_line_number(tmp_path, row):
    path = tmp_path / "bad.csv"
    path.write_text(HEADER + row + "\n", encoding="utf-8")

    with pytest.raises(ValueError, match="line 2"):
        load_tasks(path)


def test_success_keeps_stdout_and_returns_zero(capsys):
    assert run_cli(lambda: print("Study plan")) == 0
    captured = capsys.readouterr()
    assert captured.out == "Study plan\n"
    assert captured.err == ""


@pytest.mark.parametrize(
    "error",
    [
        FileNotFoundError("missing task file"),
        PermissionError("cannot read task file"),
        ValueError("Invalid importance at line 2"),
        csv.Error("malformed CSV"),
        InfeasiblePlan(7.5, 2),
    ],
)
def test_expected_failures_are_reported_to_stderr(error, capsys):
    def action():
        raise error

    assert run_cli(action) == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == f"Error: {error}\n"
    assert "Traceback" not in captured.err


def test_programming_errors_are_not_swallowed():
    def broken_pipeline():
        raise RuntimeError("unexpected bug")

    with pytest.raises(RuntimeError, match="unexpected bug"):
        run_cli(broken_pipeline)


def test_partial_allocation_is_still_allowed(tmp_path, capsys):
    path = tmp_path / "tasks.csv"
    path.write_text(VALID_CSV, encoding="utf-8")
    blocks = []

    def pipeline():
        blocks.extend(allocate(load_tasks(path), hours=2))

    assert run_cli(pipeline) == 0
    assert sum(block.hours for block in blocks) == 2
    assert capsys.readouterr().err == ""


@pytest.mark.parametrize(
    ("scenario", "content", "expected_code", "diagnostic"),
    [
        ("valid", VALID_CSV, 0, ""),
        ("missing", None, 1, "missing.csv"),
        ("empty", "", 1, "No tasks found"),
        ("header-only", HEADER, 1, "No tasks found"),
        ("invalid", HEADER + "Exam,invalid,2,2030-10-30\n", 1, "line 2"),
        ("infeasible", VALID_CSV, 1, "Plan needs 7.5 hours"),
    ],
)
def test_cli_boundary_in_a_real_process(
    tmp_path, scenario, content, expected_code, diagnostic
):
    path = tmp_path / ("missing.csv" if content is None else "tasks.csv")
    if content is not None:
        path.write_text(content, encoding="utf-8")

    # Exercise the integration contract without implementing the leader's CLI.
    script = (
        "import sys\n"
        "from shared.study_planner.errors import InfeasiblePlan, load_tasks, run_cli\n"
        "def pipeline():\n"
        "    tasks = load_tasks(sys.argv[1])\n"
        "    if sys.argv[2] == 'infeasible':\n"
        "        raise InfeasiblePlan(7.5, 2)\n"
        "    print(f'Loaded {len(tasks)} tasks')\n"
        "raise SystemExit(run_cli(pipeline))\n"
    )
    result = subprocess.run(
        [sys.executable, "-c", script, str(path), scenario],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
        timeout=10,
    )

    assert result.returncode == expected_code
    assert "Traceback" not in result.stderr
    if expected_code == 0:
        assert result.stdout == "Loaded 2 tasks\n"
        assert result.stderr == ""
    else:
        assert result.stdout == ""
        assert result.stderr.startswith("Error: ")
        assert diagnostic in result.stderr
