"""Utilities for analysing assistant request latency."""

from collections import defaultdict
from math import ceil


def analyse(pairs: list[tuple[str, float]]) -> dict:
    """Summarise request counts and latency statistics by intent."""
    grouped: dict[str, list[float]] = defaultdict(list)

    for intent, latency_ms in pairs:
        grouped[intent].append(latency_ms)

    counts = {
        intent: len(latencies)
        for intent, latencies in grouped.items()
    }

    p95 = {}
    averages = {}

    for intent, latencies in grouped.items():
        ordered = sorted(latencies)

        # Nearest-rank method for the 95th percentile.
        index = ceil(0.95 * len(ordered)) - 1
        p95[intent] = ordered[index]

        averages[intent] = sum(latencies) / len(latencies)

    slowest = max(averages, key=lambda intent: averages[intent]) if averages else None

    return {
        "counts": counts,
        "slowest": slowest,
        "p95": p95,
    }