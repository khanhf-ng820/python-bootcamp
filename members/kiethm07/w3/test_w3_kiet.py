"""Focused unit tests for kiethm07 Week 3 individual exercises."""

import subprocess
import sys
from datetime import date
from pathlib import Path

import pytest

from members.kiethm07.w3.dates import parse_due
from members.kiethm07.w3.log_stats import analyse

BOOTCAMP_ROOT = Path(__file__).resolve().parents[3]
TODAY = date(2026, 10, 6)  # Tuesday


def test_parse_due_formats():
    """Verify ISO, today, tomorrow, and relative day patterns."""
    assert parse_due("2026-12-25", TODAY) == date(2026, 12, 25)
    assert parse_due("today", TODAY) == TODAY
    assert parse_due("tomorrow", TODAY) == date(2026, 10, 7)
    assert parse_due("in 1 day", TODAY) == date(2026, 10, 7)
    assert parse_due("in 5 days", TODAY) == date(2026, 10, 11)


def test_parse_due_weekdays():
    """Verify upcoming weekday calculation, ensuring current weekday wraps to next week."""
    assert parse_due("Wed", TODAY) == date(2026, 10, 7)
    assert parse_due("Wednesday", TODAY) == date(2026, 10, 7)
    assert parse_due("Fri", TODAY) == date(2026, 10, 9)
    # Today is Tuesday: next Tue must be 7 days later
    assert parse_due("Tue", TODAY) == date(2026, 10, 13)
    assert parse_due("Tuesday", TODAY) == date(2026, 10, 13)


def test_parse_due_invalid():
    """Verify invalid strings and empty inputs raise ValueError."""
    with pytest.raises(ValueError):
        parse_due("", TODAY)
    with pytest.raises(ValueError):
        parse_due("next week", TODAY)
    with pytest.raises(ValueError):
        parse_due("invalid-date", TODAY)


def test_log_stats_empty():
    """Verify analyse handles empty pair collections gracefully."""
    res = analyse([])
    assert res["counts"] == {}
    assert res["p95"] == {}
    assert res["slowest"] == ""


def test_log_stats_calculations():
    """Verify frequency count, nearest-rank p95, and slowest route identification."""
    data = [
        ("api/v1/auth", 120),
        ("api/v1/auth", 150),
        ("api/v1/users", 450),
        ("api/v1/users", 200),
        ("api/v1/users", 600),
    ]
    res = analyse(data)
    assert res["counts"]["api/v1/auth"] == 2
    assert res["counts"]["api/v1/users"] == 3
    # users: [200, 450, 600] -> rank ceil(0.95*3) = 3 -> 600
    assert res["p95"]["api/v1/users"] == 600
    assert res["slowest"] == "api/v1/users"


def test_cli_execution():
    """Verify CLI end-to-end execution with hours, reference date, and missing file error."""
    cli_cmd = [
        sys.executable,
        "-m",
        "members.kiethm07.w3.cli",
        str(BOOTCAMP_ROOT / "samples" / "tasks.csv"),
        "--hours",
        "3",
        "--today",
        "2026-10-26",
    ]
    result = subprocess.run(cli_cmd, capture_output=True, text=True, check=False)
    assert result.returncode == 0
    assert "Tonight (3.0 h):" in result.stdout
    assert "Assignment" in result.stdout

    missing_cmd = [
        sys.executable,
        "-m",
        "members.kiethm07.w3.cli",
        "nonexistent_tasks.csv",
        "--hours",
        "2",
    ]
    bad_res = subprocess.run(missing_cmd, capture_output=True, text=True, check=False)
    assert bad_res.returncode == 1
