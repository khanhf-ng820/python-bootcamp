"""Tests for shared.study_planner.export."""

import json
from datetime import date

import pytest

from shared.contract import Block, Task
from shared.study_planner.export import export_plan


def _sample_blocks() -> list[Block]:
    exam = Task(
        title="DS exam",
        importance=5,
        effort_h=6.0,
        deadline=date(2026, 10, 30),
    )
    assignment = Task(
        title="Assignment | part 1",
        importance=4,
        effort_h=1.5,
        deadline=date(2026, 10, 27),
    )
    return [Block(task=exam, hours=6.0), Block(task=assignment, hours=1.5)]


def _sample_summary() -> dict:
    return {
        "total_tasks": 2,
        "total_effort_h": 7.5,
        "allocated_hours": 7.5,
        "remaining_hours": 0.0,
        "completion_rate": 100.0,
        "overdue_tasks": [],
    }


def test_export_plan_writes_json(tmp_path):
    output = tmp_path / "nested" / "plan.json"

    result = export_plan(_sample_blocks(), output, _sample_summary())

    assert result == output
    data = json.loads(output.read_text(encoding="utf-8"))
    assert data["total_hours"] == 7.5
    assert len(data["blocks"]) == 2
    assert data["blocks"][0] == {
        "index": 1,
        "title": "DS exam",
        "importance": 5,
        "effort_h": 6.0,
        "deadline": "2026-10-30",
        "hours": 6.0,
    }
    assert data["summary"]["completion_rate"] == 100.0


def test_export_plan_without_summary(tmp_path):
    output = tmp_path / "plan.json"

    export_plan(_sample_blocks(), output)

    data = json.loads(output.read_text(encoding="utf-8"))
    assert data["summary"] is None


def test_export_plan_writes_markdown(tmp_path):
    output = tmp_path / "plan.md"

    export_plan(_sample_blocks(), output, _sample_summary())

    text = output.read_text(encoding="utf-8")
    assert text.startswith("# Study Plan")
    assert "| # | Task | Importance | Deadline | Effort (h) | Allocated (h) |" in text
    assert r"Assignment \| part 1" in text
    assert "## Summary" in text
    assert "- Total Tasks: 2" in text
    assert "- Completion Rate: 100.0%" in text
    assert "Overdue Tasks" not in text


def test_export_plan_empty_plan(tmp_path):
    output = tmp_path / "plan.md"

    export_plan([], output)

    text = output.read_text(encoding="utf-8")
    assert "_No study blocks scheduled._" in text
    assert "| # |" not in text


def test_export_plan_explicit_format_overrides_suffix(tmp_path):
    output = tmp_path / "plan.txt"

    export_plan(_sample_blocks(), output, fmt="md")

    assert output.read_text(encoding="utf-8").startswith("# Study Plan")


def test_export_plan_unknown_suffix_raises(tmp_path):
    with pytest.raises(ValueError, match="Unsupported export suffix"):
        export_plan(_sample_blocks(), tmp_path / "plan.txt")


def test_export_plan_unknown_format_raises(tmp_path):
    with pytest.raises(ValueError, match="Unsupported export format"):
        export_plan(_sample_blocks(), tmp_path / "plan.json", fmt="yaml")
