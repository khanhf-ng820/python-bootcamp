"""Unit tests for shared allocate function (Team T-W2)."""

from datetime import date, timedelta

import pytest

from shared.contract import Block, Task
from shared.study_planner.allocate import allocate
from shared.study_planner.prioritise import prioritise
from shared.study_planner.summary import summarise

TODAY = date(2026, 10, 26)


def make_task(title: str, importance: int, effort_h: float, days_left: int = 5) -> Task:
    return Task(
        title=title,
        importance=importance,
        effort_h=effort_h,
        deadline=TODAY + timedelta(days=days_left),
    )


def test_allocate_exact_hours():
    t1 = make_task("Task 1", 5, 3.0)
    t2 = make_task("Task 2", 3, 2.0)

    blocks = allocate([t1, t2], 5.0)

    assert len(blocks) == 2
    assert blocks[0] == Block(t1, 3.0)
    assert blocks[1] == Block(t2, 2.0)


def test_allocate_partial_hours():
    t1 = make_task("Math Exam", 5, 4.0)
    t2 = make_task("Physics Lab", 4, 3.0)

    blocks = allocate([t1, t2], 5.5)

    assert len(blocks) == 2
    assert blocks[0] == Block(t1, 4.0)
    assert blocks[1] == Block(t2, 1.5)


def test_allocate_cuts_off_when_hours_exhausted():
    t1 = make_task("First", 5, 2.0)
    t2 = make_task("Second", 4, 3.0)
    t3 = make_task("Third", 3, 4.0)

    blocks = allocate([t1, t2, t3], 2.0)

    assert len(blocks) == 1
    assert blocks[0] == Block(t1, 2.0)


def test_allocate_excess_hours():
    t1 = make_task("Easy Task", 2, 1.0)
    t2 = make_task("Medium Task", 3, 2.5)

    blocks = allocate([t1, t2], 10.0)

    assert len(blocks) == 2
    assert blocks[0] == Block(t1, 1.0)
    assert blocks[1] == Block(t2, 2.5)
    assert sum(b.hours for b in blocks) == 3.5


def test_allocate_empty_tasks():
    assert allocate([], 5.0) == []


def test_allocate_zero_hours():
    t = make_task("Task", 3, 2.0)
    assert allocate([t], 0.0) == []


def test_allocate_skips_zero_effort_tasks():
    t_zero = make_task("Zero Effort", 1, 0.0)
    t_normal = make_task("Normal Effort", 4, 3.0)

    blocks = allocate([t_zero, t_normal], 2.0)

    assert len(blocks) == 1
    assert blocks[0] == Block(t_normal, 2.0)


def test_allocate_negative_hours_raises_value_error():
    t = make_task("Task", 3, 2.0)
    with pytest.raises(ValueError, match="Available hours cannot be negative"):
        allocate([t], -1.0)


def test_allocate_negative_effort_raises_value_error():
    t = make_task("Task", 3, 2.0)
    t.effort_h = -2.0
    with pytest.raises(ValueError, match="Task effort cannot be negative"):
        allocate([t], 5.0)


def test_allocate_preserves_task_order():
    tasks = [
        make_task("A", 1, 1.0),
        make_task("B", 5, 1.0),
        make_task("C", 3, 1.0),
    ]
    blocks = allocate(tasks, 2.0)

    assert len(blocks) == 2
    assert blocks[0].task.title == "A"
    assert blocks[1].task.title == "B"


def test_allocate_does_not_modify_input_tasks():
    t1 = make_task("Task 1", 4, 3.0)
    t2 = make_task("Task 2", 3, 2.0)
    original_tasks = [t1, t2]
    tasks_copy = [t1, t2]

    allocate(tasks_copy, 1.5)

    assert tasks_copy == original_tasks
    assert t1.effort_h == 3.0
    assert t2.effort_h == 2.0


def test_allocate_with_iterable_generator():
    def task_generator():
        yield make_task("Gen 1", 3, 2.0)
        yield make_task("Gen 2", 4, 1.0)

    blocks = allocate(task_generator(), 2.5)

    assert len(blocks) == 2
    assert blocks[0].hours == 2.0
    assert blocks[1].hours == 0.5


def test_integration_prioritise_allocate_summarise():
    t_later = make_task("Later Task", 2, 4.0, days_left=10)
    t_urgent = make_task("Urgent Task", 5, 3.0, days_left=1)

    sorted_tasks = prioritise([t_later, t_urgent], TODAY)
    assert sorted_tasks[0].title == "Urgent Task"

    blocks = allocate(sorted_tasks, 4.0)
    assert len(blocks) == 2
    assert blocks[0].task.title == "Urgent Task"
    assert blocks[0].hours == 3.0
    assert blocks[1].task.title == "Later Task"
    assert blocks[1].hours == 1.0

    summary = summarise(sorted_tasks, blocks)
    assert summary["total_tasks"] == 2
    assert summary["total_effort_h"] == 7.0
    assert summary["allocated_hours"] == 4.0
    assert summary["remaining_hours"] == 3.0
    assert summary["completion_rate"] == 57.14
