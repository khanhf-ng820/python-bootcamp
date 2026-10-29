"""Study allocation statistics aggregation and formatting for CLI --stats (Team T-W3)."""

from __future__ import annotations

from collections import Counter, defaultdict
from collections.abc import Iterable
from typing import Any, TypedDict

from shared.contract import Block


class AllocationStats(TypedDict):
    """Structured study allocation metrics."""

    total_hours: float
    total_blocks: int
    hours_by_importance: dict[int, float]
    blocks_by_importance: dict[int, int]
    hours_by_task: dict[str, float]
    percentage_by_importance: dict[int, float]
    top_task: tuple[str, float] | None


def calculate_stats(blocks: Iterable[Block]) -> AllocationStats:
    """Aggregate study plan metrics using Counter and defaultdict.

    Calculates:
    - total_hours: Sum of all allocated hours.
    - total_blocks: Total number of scheduled blocks.
    - hours_by_importance: Total allocated hours grouped by importance level (1-5).
    - blocks_by_importance: Number of scheduled blocks per importance level (Counter).
    - hours_by_task: Total allocated hours for each distinct task title.
    - percentage_by_importance: Percentage share of total time per importance level.
    - top_task: Tuple of (title, allocated_hours) for the highest-effort task.

    Args:
        blocks: Iterable collection of Block instances.

    Returns:
        An AllocationStats mapping with aggregated metrics.
    """
    block_list = list(blocks)
    total_hours = round(sum(b.hours for b in block_list), 2)
    total_blocks = len(block_list)

    hours_by_imp: defaultdict[int, float] = defaultdict(float)
    blocks_by_imp: Counter[int] = Counter()
    hours_by_task: defaultdict[str, float] = defaultdict(float)

    for block in block_list:
        imp = block.task.importance
        hours = block.hours
        title = block.task.title

        hours_by_imp[imp] = round(hours_by_imp[imp] + hours, 2)
        blocks_by_imp[imp] += 1
        hours_by_task[title] = round(hours_by_task[title] + hours, 2)

    pct_by_imp: dict[int, float] = {}
    if total_hours > 0:
        for imp, hours in hours_by_imp.items():
            pct_by_imp[imp] = round((hours / total_hours) * 100.0, 1)

    top_task: tuple[str, float] | None = None
    if hours_by_task:
        top_task_title = max(hours_by_task, key=lambda t: (hours_by_task[t], t))
        top_task = (top_task_title, hours_by_task[top_task_title])

    # Convert to sorted dicts for deterministic ordering (importance descending: 5 down to 1)
    sorted_hours_imp = {k: hours_by_imp[k] for k in sorted(hours_by_imp, reverse=True)}
    sorted_blocks_imp = {k: blocks_by_imp[k] for k in sorted(blocks_by_imp, reverse=True)}
    sorted_pct_imp = {k: pct_by_imp[k] for k in sorted(pct_by_imp, reverse=True)}

    return {
        "total_hours": total_hours,
        "total_blocks": total_blocks,
        "hours_by_importance": sorted_hours_imp,
        "blocks_by_importance": sorted_blocks_imp,
        "hours_by_task": dict(hours_by_task),
        "percentage_by_importance": sorted_pct_imp,
        "top_task": top_task,
    }


def format_stats(
    stats_or_blocks: AllocationStats | dict[str, Any] | Iterable[Block],
) -> str:
    """Format allocation statistics into human-readable text for CLI output.

    Accepts either an existing AllocationStats dictionary or an iterable of Block items.

    Args:
        stats_or_blocks: Precomputed stats dictionary or iterable of Block objects.

    Returns:
        Formatted multi-line statistics summary string.
    """
    if isinstance(stats_or_blocks, dict):
        stats = stats_or_blocks
    else:
        stats = calculate_stats(stats_or_blocks)

    lines: list[str] = ["Study Plan Statistics:"]

    total_blocks = stats.get("total_blocks", 0)
    total_hours = stats.get("total_hours", 0.0)

    if total_blocks == 0 or total_hours <= 0:
        lines.append("  - No allocated study blocks to analyze.")
        return "\n".join(lines)

    lines.append(f"  - Total Allocated: {total_hours:.1f} h across {total_blocks} block(s)")

    top_task = stats.get("top_task")
    if top_task:
        lines.append(f"  - Top Task: {top_task[0]} ({top_task[1]:.1f} h)")

    hours_by_imp = stats.get("hours_by_importance", {})
    blocks_by_imp = stats.get("blocks_by_importance", {})
    pct_by_imp = stats.get("percentage_by_importance", {})

    if hours_by_imp:
        lines.append("  - Breakdown by Importance:")
        for imp in sorted(hours_by_imp.keys(), reverse=True):
            hours = hours_by_imp[imp]
            blocks_cnt = blocks_by_imp.get(imp, 0)
            pct = pct_by_imp.get(imp, 0.0)
            lines.append(
                f"    * Level {imp}: {hours:.1f} h ({pct:.1f}%) - {blocks_cnt} block(s)"
            )

    return "\n".join(lines)
