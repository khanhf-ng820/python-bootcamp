"""W3-2: Summarise request counts and route latency percentiles."""

from collections import Counter, defaultdict
from math import ceil


def analyse(pairs: list[tuple[str, float]]) -> dict[str, object]:
    """Return route counts, nearest-rank p95 values, and the slowest route.

    The slowest route has the highest p95; ties keep first-seen order.
    Empty input produces empty dictionaries and slowest=None.
    """
    counts = Counter(route for route, _ in pairs)
    latencies: dict[str, list[float]] = defaultdict(list)
    for route, latency in pairs:
        latencies[route].append(latency)

    p95 = {
        route: sorted(values)[ceil(0.95 * len(values)) - 1]
        for route, values in latencies.items()
    }
    slowest = max(p95, key=lambda route: p95[route], default=None)
    return {"counts": dict(counts), "p95": p95, "slowest": slowest}
