"""Focused tests for Tran Phuc Khanh's individual Week 3 exercises."""

from datetime import date

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
