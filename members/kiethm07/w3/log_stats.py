"""Latency and request statistics for service endpoints (W3-2)."""

import math
from collections import Counter, defaultdict
from collections.abc import Iterable
from typing import Any, TypedDict


class LogStats(TypedDict):
    """Aggregated metrics representation for service route logs."""

    counts: dict[str, int]
    p95: dict[str, int | float]
    slowest: str


def analyse(pairs: Iterable[tuple[str, int | float]]) -> LogStats | dict[str, Any]:
    """Compute request counts, p95 latencies, and identify the slowest route.

    Args:
        pairs: Iterable of (route, latency_ms) tuples.

    Returns:
        Dictionary with:
            - 'counts': dict mapping route name to total request count
            - 'p95': dict mapping route to 95th percentile latency (nearest-rank)
            - 'slowest': route name with the highest p95 latency (or '' if empty)
    """
    pairs_list = list(pairs)
    if not pairs_list:
        return {"counts": {}, "p95": {}, "slowest": ""}

    counts = dict(Counter(route for route, _ in pairs_list))

    latencies_by_route: dict[str, list[int | float]] = defaultdict(list)
    for route, latency in pairs_list:
        latencies_by_route[route].append(latency)

    p95: dict[str, int | float] = {}
    for route, latencies in latencies_by_route.items():
        sorted_lats = sorted(latencies)
        rank = math.ceil(0.95 * len(sorted_lats))
        idx = max(0, min(rank - 1, len(sorted_lats) - 1))
        p95[route] = sorted_lats[idx]

    slowest = max(p95, key=lambda r: (p95[r], r)) if p95 else ""

    return {
        "counts": counts,
        "p95": p95,
        "slowest": slowest,
    }
