"""Tests for the shared prioritise() function (Team T-W2)."""

from datetime import date, timedelta

from shared.contract import Task
from shared.study_planner.prioritise import prioritise

TODAY = date(2026, 10, 26)


def task(title: str, importance: int, days_left: int) -> Task:
    return Task(title, importance, 1.0, TODAY + timedelta(days=days_left))


def test_sorts_by_importance_divided_by_days_left():
    soon = task("soon", 4, 2)  # 4 / 2 = 2.0
    important = task("important", 5, 5)  # 5 / 5 = 1.0
    later = task("later", 3, 6)  # 3 / 6 = 0.5
    low = task("low", 1, 10)  # 1 / 10 = 0.1

    result = prioritise([later, low, soon, important], TODAY)

    assert [t.title for t in result] == ["soon", "important", "later", "low"]


def test_does_not_modify_input_list():
    tasks = [task("a", 2, 5), task("b", 5, 1)]
    original = list(tasks)

    prioritise(tasks, TODAY)

    assert tasks == original


def test_tasks_due_today_or_overdue_come_first():
    overdue = task("overdue", 1, -2)
    due_today = task("due today", 2, 0)
    future = task("future", 5, 1)  # 5.0, but still not due yet

    result = prioritise([future, overdue, due_today], TODAY)

    assert [t.title for t in result] == ["due today", "overdue", "future"]


def test_equal_scores_keep_input_order():
    first = task("first", 4, 2)  # 2.0
    second = task("second", 2, 1)  # 2.0

    result = prioritise([first, second], TODAY)

    assert [t.title for t in result] == ["first", "second"]


def test_empty_list_returns_empty_list():
    assert prioritise([], TODAY) == []
