"""Latency and request statistics for service endpoints."""

import math
from collections import Counter, defaultdict
from typing import Any


def analyse(pairs: list[tuple[str, int]]) -> dict[str, Any]:
    """Compute request counts, p95 latencies, and identify the slowest route.

    Args:
        pairs: List of (route, latency_ms) tuples.

    Returns:
        Dictionary with:
            - "counts": dict mapping route to total request count
            - "p95": dict mapping route to 95th percentile latency (nearest rank)
            - "slowest": the route name with the highest p95 latency (or "" if empty)
    """
    if not pairs:
        return {"counts": {}, "p95": {}, "slowest": ""}

    counts = dict(Counter(route for route, _ in pairs))

    latencies_by_route: dict[str, list[int]] = defaultdict(list)
    for route, latency in pairs:
        latencies_by_route[route].append(latency)

    p95: dict[str, int] = {}
    for route, latencies in latencies_by_route.items():
        sorted_lats = sorted(latencies)
        rank = math.ceil(0.95 * len(sorted_lats))
        idx = max(0, min(rank - 1, len(sorted_lats) - 1))
        p95[route] = sorted_lats[idx]

    slowest = max(p95, key=p95.get) if p95 else ""

    return {
        "counts": counts,
        "p95": p95,
        "slowest": slowest,
    }
