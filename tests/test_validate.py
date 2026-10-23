"""Acceptance tests for Study Planner task validation (issue #31)."""

from dataclasses import asdict
from datetime import date, timedelta

import pytest

from shared.contract import Task
from shared.study_planner.validate import validate_tasks

TODAY = date(2026, 10, 23)


def test_valid_future_tasks_are_retained():
    tasks = [
        Task("Exam", 5, 6.0, TODAY + timedelta(days=7)),
        Task("Assignment", 4, 1.5, TODAY + timedelta(days=4)),
    ]
    assert validate_tasks(tasks, TODAY) == tasks


@pytest.mark.parametrize("days, retained", [(-1, False), (0, True), (1, True)])
def test_deadline_boundary(days, retained):
    task = Task("Review", 3, 1.0, TODAY + timedelta(days=days))
    assert validate_tasks([task], TODAY) == ([task] if retained else [])


@pytest.mark.parametrize("importance, retained", [(0, False), (1, True), (5, True), (6, False)])
def test_importance_range(importance, retained):
    task = Task("Review", 3, 1.0, TODAY)
    # The constructor rejects invalid importance; exercise a mutated Task.
    task.importance = importance
    assert validate_tasks([task], TODAY) == ([task] if retained else [])


@pytest.mark.parametrize("effort, retained", [(-1.0, False), (0.0, True), (1.5, True)])
def test_effort_range(effort, retained):
    task = Task("Review", 3, effort, TODAY)
    assert validate_tasks([task], TODAY) == ([task] if retained else [])


def test_mixed_input_keeps_valid_objects_in_original_order():
    later = Task("Later", 1, 2.0, TODAY + timedelta(days=3))
    overdue = Task("Late", 5, 1.0, TODAY - timedelta(days=1))
    due_today = Task("Today", 5, 0.0, TODAY)
    invalid_importance = Task("Invalid importance", 3, 1.0, TODAY)
    invalid_importance.importance = 6
    negative_effort = Task("Negative effort", 3, -2.0, TODAY)

    result = validate_tasks(
        [later, overdue, invalid_importance, due_today, negative_effort], TODAY
    )

    assert len(result) == 2
    assert result[0] is later
    assert result[1] is due_today


def test_empty_input_returns_new_empty_list():
    tasks = []
    result = validate_tasks(tasks, TODAY)
    assert result == []
    assert result is not tasks


def test_all_invalid_tasks_return_empty_list():
    tasks = [
        Task("Late", 3, 1.0, TODAY - timedelta(days=1)),
        Task("Negative", 3, -1.0, TODAY),
    ]
    assert validate_tasks(tasks, TODAY) == []


def test_validation_does_not_modify_input_list_or_task_fields():
    tasks = [
        Task("Valid", 3, 1.0, TODAY),
        Task("Overdue", 5, 2.0, TODAY - timedelta(days=1)),
    ]
    original_objects = tasks.copy()
    original_fields = [asdict(task) for task in tasks]

    result = validate_tasks(tasks, TODAY)
    result.clear()

    assert len(tasks) == len(original_objects)
    assert all(task is original for task, original in zip(tasks, original_objects))
    assert [asdict(task) for task in tasks] == original_fields


def test_uses_supplied_today_instead_of_system_date():
    supplied_today = date(2000, 1, 1)
    task = Task("Historical plan", 3, 1.0, supplied_today)
    assert validate_tasks([task], supplied_today) == [task]
