"""Compute chat-log statistics such as counts and p95 latency (W3-2)."""

import math
from collections import Counter, defaultdict
from collections.abc import Iterable
from typing import TypedDict


class LogStats(TypedDict):
    """Aggregated statistics for a list of route/latency pairs."""

    counts: Counter[str]
    p95: dict[str, float]
    slowest: str | None


def analyse(pairs: Iterable[tuple[str, float]]) -> LogStats:
    """Summarise request counts and p95 latency per route.

    ``p95`` uses the nearest-rank definition: for a route with ``n``
    samples the value is the sample at position ``ceil(0.95 * n)`` in the
    sorted list. ``slowest`` is the route with the highest p95, or ``None``
    when there are no pairs.

    Args:
        pairs: An iterable of ``(route, latency_ms)`` pairs.

    Returns:
        A mapping with ``counts``, ``p95`` and ``slowest`` entries.
    """
    counts: Counter[str] = Counter()
    latencies: defaultdict[str, list[float]] = defaultdict(list)

    for route, latency_ms in pairs:
        counts[route] += 1
        latencies[route].append(latency_ms)

    p95 = {route: _p95(values) for route, values in latencies.items()}
    slowest = max(p95, key=lambda route: (p95[route], route), default=None)

    return {"counts": counts, "p95": p95, "slowest": slowest}


def _p95(values: list[float]) -> float:
    """Return the nearest-rank 95th percentile of ``values``."""
    ordered = sorted(values)
    rank = math.ceil(0.95 * len(ordered))
    return ordered[max(rank - 1, 0)]
