"""Focused tests for Tran Phuc Khanh's individual Week 3 exercises."""

import subprocess
import sys
from datetime import date
from pathlib import Path

import pytest

from .dates import parse_due
from .log_stats import analyse

TODAY = date(2026, 10, 6)


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("2026-10-30", date(2026, 10, 30)),
        ("2028-02-29", date(2028, 2, 29)),
        ("tomorrow", date(2026, 10, 7)),
        ("in 3 days", date(2026, 10, 9)),
        ("in 0 days", TODAY),
        ("in 1 day", date(2026, 10, 7)),
        ("Fri", date(2026, 10, 9)),
        ("Tuesday", date(2026, 10, 13)),
        (" Mon ", date(2026, 10, 12)),
    ],
)
def test_parse_due_formats(text: str, expected: date) -> None:
    """Resolve each supported date format from a supplied reference date."""
    assert parse_due(text, TODAY) == expected


@pytest.mark.parametrize(
    "text", ["someday", "", "2026-02-30", "in -3 days", "Friyay", "20261030"]
)
def test_parse_due_rejects_invalid_text(text: str) -> None:
    """Reject unknown or invalid date expressions."""
    with pytest.raises(ValueError):
        parse_due(text, TODAY)


def test_tomorrow_crosses_year_boundary() -> None:
    """Use date arithmetic correctly across the end of a year."""
    assert parse_due("tomorrow", date(2026, 12, 31)) == date(2027, 1, 1)


def test_analyse_groups_request_counts_and_latencies() -> None:
    """Summarise counts and the highest p95 across different routes."""
    pairs = [("fee", 100), ("fee", 300), ("rag", 900), ("rag", 1100), ("fee", 200)]
    assert analyse(pairs) == {
        "counts": {"fee": 3, "rag": 2},
        "p95": {"fee": 300, "rag": 1100},
        "slowest": "rag",
    }


@pytest.mark.parametrize(
    ("latencies", "expected"),
    [([7], 7), (list(range(1, 21)), 19), (list(range(1, 22)), 20)],
)
def test_p95_uses_nearest_rank(latencies: list[int], expected: int) -> None:
    """Choose the ceiling rank correctly at and between percentile boundaries."""
    assert analyse([("fee", value) for value in latencies])["p95"] == {"fee": expected}


def test_slowest_route_is_selected_by_p95() -> None:
    """A single outlier must not replace the route with the highest p95."""
    pairs = [("outlier", 0)] * 19 + [("outlier", 1000), ("steady", 100)]
    assert analyse(pairs)["slowest"] == "steady"


def test_analyse_empty_input() -> None:
    """Describe an empty log without an arbitrary slowest route."""
    assert analyse([]) == {"counts": {}, "p95": {}, "slowest": None}


def test_analyse_keeps_original_pairs() -> None:
    """Sorting latency samples must leave the supplied pairs unchanged."""
    pairs = [("fee", 300), ("rag", 100), ("fee", 10)]
    original = pairs.copy()
    analyse(pairs)
    assert pairs == original


ROOT = Path(__file__).resolve().parents[3]


def _run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    """Run the member CLI with captured process output."""
    return subprocess.run(
        [sys.executable, "-m", "members.TranPhucKhanhh.w3.cli", *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
        timeout=10,
    )


def test_cli_sample_schedule() -> None:
    """Reuse W2 tasks to reproduce the tutorial's partial two-hour plan."""
    result = _run_cli(
        str(ROOT / "samples/tasks.csv"), "--hours", "2", "--today", "2026-10-26"
    )
    assert result.returncode == 0
    assert result.stdout == (
        "Tonight (2.0 h):\n  1. Assignment ...... 1.5 h\n  2. DS exam ...... 0.5 h\n"
    )
    assert result.stderr == ""


def test_cli_missing_file() -> None:
    """Return exit code 1 and a readable diagnostic for a missing CSV."""
    result = _run_cli(str(ROOT / "missing-w3-input.csv"), "--hours", "2")
    assert result.returncode == 1
    assert result.stdout == ""
    assert "missing-w3-input.csv" in result.stderr
    assert "Traceback" not in result.stderr


def test_cli_invalid_csv_keeps_line_number(tmp_path: Path) -> None:
    """Report the W2 loader's row error without a traceback."""
    path = tmp_path / "invalid.csv"
    path.write_text(
        "title,importance,effort_h,deadline\nExam,invalid,2,2026-10-30\n",
        encoding="utf-8",
    )
    result = _run_cli(str(path), "--hours", "2")
    assert result.returncode == 1
    assert "line 2" in result.stderr
    assert "Traceback" not in result.stderr


@pytest.mark.parametrize("hours", ["-1", "abc", "nan", "inf"])
def test_cli_rejects_invalid_hours(hours: str) -> None:
    """Reject unusable time budgets at the argument boundary."""
    result = _run_cli(str(ROOT / "samples/tasks.csv"), "--hours", hours)
    assert result.returncode == 2
    assert "--hours" in result.stderr
    assert "Traceback" not in result.stderr


def test_cli_rejects_invalid_reference_date() -> None:
    """Let argparse report an invalid --today value cleanly."""
    result = _run_cli(
        str(ROOT / "samples/tasks.csv"), "--hours", "2", "--today", "not-a-date"
    )
    assert result.returncode == 2
    assert "--today" in result.stderr
    assert "Traceback" not in result.stderr


def test_cli_today_is_optional() -> None:
    """Allow callers to use the actual current date by omitting --today."""
    result = _run_cli(str(ROOT / "samples/tasks.csv"), "--hours", "2")
    assert result.returncode == 0
    assert result.stdout.startswith("Tonight (2.0 h):")
    assert result.stderr == ""


def test_cli_reference_date_affects_priority(tmp_path: Path) -> None:
    """Use the supplied reference date when computing task priority."""
    path = tmp_path / "tasks.csv"
    path.write_text(
        "title,importance,effort_h,deadline\n"
        "Near,1,2,2026-10-31\nImportant,5,2,2026-11-10\n",
        encoding="utf-8",
    )
    early = _run_cli(str(path), "--hours", "1", "--today", "2026-10-01")
    late = _run_cli(str(path), "--hours", "1", "--today", "2026-10-30")
    assert early.returncode == late.returncode == 0
    assert "1. Important" in early.stdout
    assert "1. Near" in late.stdout
