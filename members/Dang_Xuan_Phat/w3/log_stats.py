"""Compute chat log statistics including route frequencies and p95 latency (W3-2)."""

from __future__ import annotations

import math
from collections import Counter, defaultdict
from collections.abc import Iterable
from typing import TypedDict


class LogStats(TypedDict):
    """Structured dictionary representation of chat log metrics."""

    counts: Counter[str]
    p95: dict[str, float]
    slowest: str | None


def analyse(pairs: Iterable[tuple[str, float]]) -> LogStats:
    """Analyze a collection of (route, latency_ms) records.

    Calculates:
    - counts: Number of requests handled by each route (Counter).
    - p95: Nearest-rank 95th percentile latency per route.
    - slowest: Name of the route with the highest p95 latency (or None if empty).

    Args:
        pairs: Iterable containing (route, latency_ms) tuples.

    Returns:
        A LogStats mapping with 'counts', 'p95', and 'slowest' fields.
    """
    counts: Counter[str] = Counter()
    latencies: defaultdict[str, list[float]] = defaultdict(list)

    for route, latency in pairs:
        counts[route] += 1
        latencies[route].append(float(latency))

    p95: dict[str, float] = {}
    for route, values in latencies.items():
        p95[route] = _calculate_p95(values)

    slowest: str | None = None
    if p95:
        slowest = max(p95, key=lambda r: (p95[r], r))

    return {
        "counts": counts,
        "p95": p95,
        "slowest": slowest,
    }


def _calculate_p95(values: list[float]) -> float:
    """Calculate the 95th percentile using the nearest-rank method."""
    if not values:
        return 0.0
    sorted_vals = sorted(values)
    rank = math.ceil(0.95 * len(sorted_vals))
    idx = max(0, min(rank - 1, len(sorted_vals) - 1))
    return sorted_vals[idx]
