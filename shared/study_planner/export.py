"""Export a study plan to JSON or Markdown (Team T-W3)."""

import json
from collections.abc import Iterable
from pathlib import Path

from shared.contract import Block

_JSON_FORMATS = {"json"}
_MARKDOWN_FORMATS = {"md", "markdown"}
_JSON_SUFFIXES = {".json"}
_MARKDOWN_SUFFIXES = {".md", ".markdown"}

_SUMMARY_LABELS = {
    "total_tasks": "Total Tasks",
    "total_effort_h": "Total Effort",
    "allocated_hours": "Allocated Hours",
    "remaining_hours": "Remaining Hours",
    "completion_rate": "Completion Rate",
}
_HOUR_KEYS = {"total_effort_h", "allocated_hours", "remaining_hours"}


def export_plan(
    blocks: Iterable[Block],
    path: str | Path,
    summary: dict | None = None,
    fmt: str | None = None,
) -> Path:
    """Write a study plan to a JSON or Markdown file.

    The output format is inferred from the file suffix (``.json``, ``.md``
    or ``.markdown``) unless ``fmt`` is given explicitly. Missing parent
    directories are created.

    Args:
        blocks: Allocated study blocks to export.
        path: Destination file for the exported plan.
        summary: Optional summary statistics from ``summarise``.
        fmt: Optional format override: ``"json"``, ``"md"`` or ``"markdown"``.

    Returns:
        The path of the written file.

    Raises:
        ValueError: If the format is unknown or the suffix is unsupported.
    """
    output_path = Path(path)
    output_format = _resolve_format(output_path, fmt)
    block_list = list(blocks)

    if output_format == "json":
        content = _to_json(block_list, summary)
    else:
        content = _to_markdown(block_list, summary)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")
    return output_path


def _resolve_format(path: Path, fmt: str | None) -> str:
    """Return ``"json"`` or ``"markdown"`` for the requested output."""
    if fmt is not None:
        name = fmt.strip().lower().lstrip(".")
        if name in _JSON_FORMATS:
            return "json"
        if name in _MARKDOWN_FORMATS:
            return "markdown"
        raise ValueError(f"Unsupported export format: {fmt!r}")

    suffix = path.suffix.lower()
    if suffix in _JSON_SUFFIXES:
        return "json"
    if suffix in _MARKDOWN_SUFFIXES:
        return "markdown"
    raise ValueError(
        f"Unsupported export suffix {suffix or '(none)'!r}; "
        "use .json, .md or .markdown"
    )


def _to_json(blocks: list[Block], summary: dict | None) -> str:
    """Serialise the plan as pretty-printed UTF-8 JSON."""
    payload = {
        "total_hours": round(sum(block.hours for block in blocks), 2),
        "blocks": [
            {
                "index": index,
                "title": block.task.title,
                "importance": block.task.importance,
                "effort_h": block.task.effort_h,
                "deadline": block.task.deadline.isoformat(),
                "hours": block.hours,
            }
            for index, block in enumerate(blocks, start=1)
        ],
        "summary": summary,
    }
    return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"


def _to_markdown(blocks: list[Block], summary: dict | None) -> str:
    """Render the plan as a Markdown document."""
    total_hours = sum(block.hours for block in blocks)
    lines = ["# Study Plan", ""]

    if not blocks:
        lines.append("_No study blocks scheduled._")
    else:
        lines.append(
            f"Total allocated: **{_format_hours(total_hours)} h** "
            f"across **{len(blocks)}** block(s)."
        )
        lines.append("")
        lines.append(
            "| # | Task | Importance | Deadline | Effort (h) | Allocated (h) |"
        )
        lines.append("|---:|:---|---:|:---|---:|---:|")
        for index, block in enumerate(blocks, start=1):
            task = block.task
            lines.append(
                f"| {index} "
                f"| {_escape_markdown(task.title)} "
                f"| {task.importance} "
                f"| {task.deadline.isoformat()} "
                f"| {_format_hours(task.effort_h)} "
                f"| {_format_hours(block.hours)} |"
            )

    if summary:
        lines.append("")
        lines.append("## Summary")
        lines.append("")
        for key, label in _SUMMARY_LABELS.items():
            if key not in summary:
                continue
            value = summary[key]
            unit = " h" if key in _HOUR_KEYS else ""
            suffix = "%" if key == "completion_rate" else unit
            lines.append(f"- {label}: {value}{suffix}")

        overdue = summary.get("overdue_tasks") or []
        if overdue:
            lines.append(f"- Overdue Tasks: {', '.join(overdue)}")

    return "\n".join(lines) + "\n"


def _format_hours(hours: float) -> str:
    """Format hours without trailing zeros (e.g. ``6`` instead of ``6.0``)."""
    return f"{round(hours, 2):g}"


def _escape_markdown(text: str) -> str:
    """Escape characters that would break a Markdown table cell."""
    return text.replace("|", r"\|")
