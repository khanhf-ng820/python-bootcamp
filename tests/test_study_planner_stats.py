"""Unit tests for study planner allocation statistics (Team T-W3)."""

from __future__ import annotations

from datetime import date

from shared.contract import Block, Task
from shared.study_planner.stats import calculate_stats, format_stats


def _make_sample_blocks() -> list[Block]:
    t1 = Task(title="Math Homework", importance=5, effort_h=4.0, deadline=date(2026, 11, 1))
    t2 = Task(title="Physics Lab", importance=4, effort_h=3.0, deadline=date(2026, 11, 2))
    t3 = Task(title="English Essay", importance=3, effort_h=2.0, deadline=date(2026, 11, 3))
    t4 = Task(title="Math Revision", importance=5, effort_h=2.0, deadline=date(2026, 11, 4))

    return [
        Block(task=t1, hours=3.0),
        Block(task=t2, hours=2.0),
        Block(task=t3, hours=1.0),
        Block(task=t4, hours=2.0),
    ]


def test_calculate_stats_totals() -> None:
    blocks = _make_sample_blocks()
    stats = calculate_stats(blocks)

    assert stats["total_hours"] == 8.0
    assert stats["total_blocks"] == 4


def test_calculate_stats_by_importance() -> None:
    blocks = _make_sample_blocks()
    stats = calculate_stats(blocks)

    # Level 5: 3.0 + 2.0 = 5.0h, 2 blocks
    # Level 4: 2.0h, 1 block
    # Level 3: 1.0h, 1 block
    assert stats["hours_by_importance"][5] == 5.0
    assert stats["hours_by_importance"][4] == 2.0
    assert stats["hours_by_importance"][3] == 1.0

    assert stats["blocks_by_importance"][5] == 2
    assert stats["blocks_by_importance"][4] == 1
    assert stats["blocks_by_importance"][3] == 1


def test_calculate_stats_percentages() -> None:
    blocks = _make_sample_blocks()
    stats = calculate_stats(blocks)

    # 5.0 / 8.0 = 62.5%
    # 2.0 / 8.0 = 25.0%
    # 1.0 / 8.0 = 12.5%
    assert stats["percentage_by_importance"][5] == 62.5
    assert stats["percentage_by_importance"][4] == 25.0
    assert stats["percentage_by_importance"][3] == 12.5


def test_calculate_stats_top_task() -> None:
    blocks = _make_sample_blocks()
    stats = calculate_stats(blocks)

    assert stats["top_task"] is not None
    assert stats["top_task"][0] == "Math Homework"
    assert stats["top_task"][1] == 3.0


def test_calculate_stats_empty() -> None:
    stats = calculate_stats([])

    assert stats["total_hours"] == 0.0
    assert stats["total_blocks"] == 0
    assert stats["hours_by_importance"] == {}
    assert stats["blocks_by_importance"] == {}
    assert stats["percentage_by_importance"] == {}
    assert stats["top_task"] is None


def test_format_stats_output() -> None:
    blocks = _make_sample_blocks()
    output = format_stats(blocks)

    assert "Study Plan Statistics:" in output
    assert "Total Allocated: 8.0 h across 4 block(s)" in output
    assert "Top Task: Math Homework (3.0 h)" in output
    assert "Level 5: 5.0 h (62.5%) - 2 block(s)" in output
    assert "Level 4: 2.0 h (25.0%) - 1 block(s)" in output
    assert "Level 3: 1.0 h (12.5%) - 1 block(s)" in output


def test_format_stats_empty() -> None:
    output = format_stats([])
    assert "No allocated study blocks to analyze." in output
