"""End-to-end tests for the shared Study Planner CLI."""

import subprocess
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
MODULE = "shared.study_planner"


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    """Execute the Study Planner CLI as a separate process."""
    return subprocess.run(
        [sys.executable, "-m", MODULE, *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
        timeout=10,
    )


def test_cli_with_sample_csv() -> None:
    """The CLI should process the sample CSV successfully."""
    result = run_cli(
        str(ROOT / "samples" / "tasks.csv"),
        "--hours", "8",
    )

    assert result.returncode == 0
    assert "DS exam" in result.stdout
    assert "Assignment" in result.stdout


def test_cli_missing_csv() -> None:
    """A missing input file should produce a clean error."""
    result = run_cli(
        str(ROOT / "samples" / "missing.csv"),
        "--hours", "2",
    )

    assert result.returncode == 1
    assert "Traceback" not in result.stderr


def test_cli_invalid_csv(tmp_path: Path) -> None:
    """Invalid CSV data should be rejected without a traceback."""
    csv_path = tmp_path / "invalid.csv"
    csv_path.write_text(
        "title,importance,effort_h,deadline\n"
        "Bad task,invalid,2,2026-10-30\n",
        encoding="utf-8",
    )

    result = run_cli(str(csv_path), "--hours", "2")

    assert result.returncode == 1
    assert "Traceback" not in result.stderr


def test_cli_empty_csv(tmp_path: Path) -> None:
    """An empty input file should fail cleanly."""
    csv_path = tmp_path / "empty.csv"
    csv_path.write_text("", encoding="utf-8")

    result = run_cli(str(csv_path), "--hours", "2")

    assert result.returncode == 1
    assert "Traceback" not in result.stderr


@pytest.mark.parametrize("hours", ["-1", "abc"])
def test_cli_invalid_hours(hours: str) -> None:
    """Negative or nonnumeric study hours should be rejected."""
    result = run_cli(
        str(ROOT / "samples" / "tasks.csv"),
        "--hours", hours,
    )

    assert result.returncode != 0