"""Unit tests for shared parse_csv function (Team T-W2)."""

from datetime import date
from pathlib import Path

import pytest

from shared.contract import Task
from shared.study_planner.parse import parse_csv

SAMPLES = Path(__file__).resolve().parents[1] / "samples"


def test_parse_sample_tasks_csv() -> None:
    tasks = parse_csv(SAMPLES / "tasks.csv")
    assert len(tasks) == 2
    assert tasks[0] == Task("DS exam", 5, 6.0, date(2026, 10, 30))
    assert tasks[1] == Task("Assignment", 4, 1.5, date(2026, 10, 27))


def test_parse_tasks_bad_csv_raises_value_error_with_line_number() -> None:
    with pytest.raises(ValueError, match="line 3"):
        parse_csv(SAMPLES / "tasks_bad.csv")


def test_parse_empty_file_returns_empty_list(tmp_path: Path) -> None:
    empty_csv = tmp_path / "empty.csv"
    empty_csv.write_text("", encoding="utf-8")
    assert parse_csv(empty_csv) == []


def test_parse_header_only_csv_returns_empty_list(tmp_path: Path) -> None:
    header_csv = tmp_path / "header_only.csv"
    header_csv.write_text("title,importance,effort_h,deadline\n", encoding="utf-8")
    assert parse_csv(header_csv) == []


def test_parse_whitespace_handling(tmp_path: Path) -> None:
    spaced_csv = tmp_path / "spaced.csv"
    spaced_csv.write_text(
        "title,importance,effort_h,deadline\n"
        "  Math Homework  ,  3  ,  2.0  ,  2026-11-05  \n",
        encoding="utf-8",
    )
    tasks = parse_csv(spaced_csv)
    assert len(tasks) == 1
    assert tasks[0] == Task("Math Homework", 3, 2.0, date(2026, 11, 5))


def test_parse_invalid_column_count_raises_value_error(tmp_path: Path) -> None:
    bad_cols = tmp_path / "bad_cols.csv"
    bad_cols.write_text("title,importance,effort_h,deadline\nMissing,3,1.0\n", encoding="utf-8")
    with pytest.raises(ValueError, match="line 2"):
        parse_csv(bad_cols)


def test_parse_invalid_importance_range_raises_value_error(tmp_path: Path) -> None:
    bad_range = tmp_path / "bad_range.csv"
    bad_range.write_text("title,importance,effort_h,deadline\nOut of bounds,9,1.0,2026-10-30\n", encoding="utf-8")
    with pytest.raises(ValueError, match="line 2"):
        parse_csv(bad_range)


def test_parse_nonexistent_file_raises_file_not_found() -> None:
    with pytest.raises(FileNotFoundError):
        parse_csv("non_existent_file.csv")
