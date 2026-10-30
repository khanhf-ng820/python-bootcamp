"""Integration tests for shared.study_planner CLI entrypoint (__main__.py)."""

import subprocess
import sys
from pathlib import Path

BOOTCAMP = Path(__file__).resolve().parents[1]
MODULE = "shared.study_planner"


def run_cli(*args: str, timeout: float = 10.0) -> subprocess.CompletedProcess[str]:
    """Execute the study planner CLI module as a subprocess."""
    return subprocess.run(
        [sys.executable, "-m", MODULE, *args],
        cwd=BOOTCAMP,
        capture_output=True,
        text=True,
        check=False,
        timeout=timeout,
    )


def test_cli_success() -> None:
    """The CLI should successfully schedule tasks from a sample CSV."""
    sample = str(BOOTCAMP / "samples" / "tasks.csv")
    res = run_cli(sample, "--hours", "2", "--today", "2026-10-26")

    assert res.returncode == 0
    assert "Assignment" in res.stdout
    assert "DS exam" in res.stdout


def test_cli_with_summary() -> None:
    """The CLI with --summary flag should append summary statistics."""
    sample = str(BOOTCAMP / "samples" / "tasks.csv")
    res = run_cli(sample, "--hours", "2", "--summary", "--today", "2026-10-26")

    assert res.returncode == 0
    assert "Summary:" in res.stdout
    assert "Total Tasks: 2" in res.stdout


def test_cli_missing_csv() -> None:
    """A non-existent CSV should exit with code 1 and clean error message."""
    res = run_cli("non_existent_tasks.csv", "--hours", "2")

    assert res.returncode == 1
    assert "not found" in res.stderr
    assert "Traceback" not in res.stderr


def test_cli_empty_csv(tmp_path: Path) -> None:
    """An empty CSV file should exit with code 1 without a traceback."""
    empty_csv = tmp_path / "empty.csv"
    empty_csv.write_text("", encoding="utf-8")
    res = run_cli(str(empty_csv), "--hours", "2")

    assert res.returncode == 1
    assert "no tasks" in res.stderr.lower()
    assert "Traceback" not in res.stderr


def test_cli_invalid_csv(tmp_path: Path) -> None:
    """A malformed CSV row should exit with code 1 without a traceback."""
    bad_csv = tmp_path / "bad.csv"
    bad_csv.write_text(
        "title,importance,effort_h,deadline\nBad,invalid_int,2,2026-10-30\n",
        encoding="utf-8",
    )
    res = run_cli(str(bad_csv), "--hours", "2")

    assert res.returncode == 1
    assert "Traceback" not in res.stderr


def test_cli_negative_effort_csv(tmp_path: Path) -> None:
    """A CSV row with negative effort should exit with code 1 without a traceback."""
    bad_csv = tmp_path / "negative_effort.csv"
    bad_csv.write_text(
        "title,importance,effort_h,deadline\nExam,5,-1,2026-11-01\n",
        encoding="utf-8",
    )
    res = run_cli(str(bad_csv), "--hours", "2")

    assert res.returncode == 1
    assert "Traceback" not in res.stderr
    assert "cannot be negative" in res.stderr.lower()


def test_cli_negative_hours() -> None:
    """Negative hours should be rejected with exit code 2."""
    sample = str(BOOTCAMP / "samples" / "tasks.csv")
    res = run_cli(sample, "--hours", "-1")

    assert res.returncode == 2
    assert "cannot be negative" in res.stderr.lower()


def test_cli_invalid_today() -> None:
    """Invalid --today format should exit with code 1 cleanly."""
    sample = str(BOOTCAMP / "samples" / "tasks.csv")
    res = run_cli(sample, "--hours", "2", "--today", "invalid-date")

    assert res.returncode == 1
    assert "invalid date" in res.stderr.lower()
    assert "Traceback" not in res.stderr
