# Study Planner CLI (`shared.study_planner`)

`shared.study_planner` is a modular Python CLI application and library designed to parse study tasks, prioritize deadlines, and greedily allocate available study hours into balanced blocks.

Developed and integrated by **Team T-W3** for the CSC10014 — Python Bootcamp course.

---

## 1. Overview & Pipeline Architecture

The application connects decoupled modules developed by team members into an end-to-end data processing pipeline from CSV input to formatted outputs:

```text
               ┌───────────────────────────────┐
               │    Input CSV (tasks.csv)      │
               └──────────────┬────────────────┘
                              │
                              ▼
               ┌───────────────────────────────┐
               │  parse_csv & validate_tasks   │
               └──────────────┬────────────────┘
                              │
                              ▼
               ┌───────────────────────────────┐
               │          prioritise           │
               └──────────────┬────────────────┘
                              │
                              ▼
               ┌───────────────────────────────┐
               │           allocate            │
               └──────────────┬────────────────┘
                              │
          ┌───────────────────┼───────────────────┐
          │                   │                   │
          ▼                   ▼                   ▼
┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
│  render (stdout) │ │  export (--output│ │  stats (--stats) │
│  ASCII table     │ │  Export to JSON  │ │  Counter &       │
│  in terminal     │ │  or Markdown     │ │  defaultdict     │
└──────────────────┘ └──────────────────┘ └──────────────────┘
```

### Pipeline Stages:
1. **`parse_csv(path)`**: Reads the CSV file and maps rows into `Task` dataclass instances.
2. **`validate_tasks(tasks)`**: Validates task constraints (importance `1` to `5`, effort `> 0`).
3. **`prioritise(tasks, today=None)`**: Ranks tasks based on importance and remaining days to deadline.
4. **`allocate(tasks, available_hours)`**: Greedily schedules study hours into `Block` items according to priority order.
5. **Output Handlers**:
   - **Terminal (Default)**: `render(blocks)` prints an aligned ASCII study schedule to stdout.
   - **File Export (`--output`)**: `export_plan(blocks, path, ...)` saves the plan to `.json` or `.md`.
   - **Statistics (`--stats`)**: `format_stats(blocks)` provides metric breakdowns aggregated via `Counter` and `defaultdict`.

---

## 2. Requirements & Environment

- **Python**: Version 3.10 or higher.
- **Dependencies**: 100% Python Standard Library (`argparse`, `csv`, `datetime`, `json`, `collections`, `dataclasses`, `pathlib`).
- Check your environment:
  ```bash
  python --version
  ```

---

## 3. Input CSV Specification

The input tasks CSV file must include the following 4 required columns with header:

| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `title` | `str` | Non-empty | Course or assignment title |
| `importance` | `int` | Integer from `1` to `5` | Priority rating (5 is highest) |
| `effort_h` | `float` | Real number `> 0` | Estimated hours needed to complete |
| `deadline` | `str` | ISO format `YYYY-MM-DD` | Due date of the task |

### Example Input (`samples/tasks.csv`):
```csv
title,importance,effort_h,deadline
DS exam,5,6.0,2026-10-30
Assignment,4,1.5,2026-10-27
Linear Algebra Quiz,3,2.0,2026-11-02
```

---

## 4. CLI Usage & Arguments

Execute the module directly from the repository root:

```bash
python -m shared.study_planner <csv_path> --hours <HOURS> [options]
```

### Options & Flags Reference

| Argument / Flag | Required | Default | Description |
| :--- | :---: | :---: | :--- |
| `csv_path` | **Yes** | *(None)* | Path to tasks CSV file (e.g. `samples/tasks.csv`). |
| `--hours <float>` | **Yes** | *(None)* | Total available study hours to allocate (must be positive). |
| `--today <YYYY-MM-DD>` | No | Current date | Reference date used to calculate urgency and days left. |
| `--output <path>` | No | `None` | Output destination file. Format is inferred from `.json`, `.md`, or `.markdown`. |
| `--stats` | No | `False` | Show aggregated allocation statistics (hours, blocks, shares, top task). |

---

## 5. Common Usage Scenarios

### 5.1. Basic Allocation (Standard Output)
Allocate 8 study hours and print the schedule:
```bash
python -m shared.study_planner samples/tasks.csv --hours 8
```
**Sample Output:**
```text
=== Study Plan ===
Available hours: 8.00 h
Total allocated: 7.50 h

#1 | DS exam             | 6.00 h | Imp: 5 | Due: 2026-10-30
#2 | Assignment          | 1.50 h | Imp: 4 | Due: 2026-10-27
```

### 5.2. Reference Date Flag (`--today`)
Prioritize tasks relative to a custom baseline date:
```bash
python -m shared.study_planner samples/tasks_extended.csv --hours 10 --today 2026-10-28
```

### 5.3. Display Allocation Statistics (`--stats`)
View metric aggregation across importance levels:
```bash
python -m shared.study_planner samples/tasks_extended.csv --hours 12 --stats
```
**Sample Statistics Block:**
```text
Study Plan Statistics:
  - Total Allocated: 12.0 h across 4 block(s)
  - Top Task: Data Structures Final Exam (6.0 h)
  - Breakdown by Importance:
    * Level 5: 10.0 h (83.3%) - 2 block(s)
    * Level 4: 2.0 h (16.7%) - 2 block(s)
```

### 5.4. Export Plan to Markdown (`--output plan.md`)
```bash
python -m shared.study_planner samples/tasks.csv --hours 6 --output output/my_plan.md
```
Automatically generates parent folders and writes standard Markdown:
```markdown
# Study Plan

Total allocated: **6 h** across **2** block(s).

| # | Task | Importance | Deadline | Effort (h) | Allocated (h) |
|---:|:---|---:|:---|---:|---:|
| 1 | DS exam | 5 | 2026-10-30 | 6 | 6 |
```

### 5.5. Export Plan to JSON (`--output plan.json`)
```bash
python -m shared.study_planner samples/tasks.csv --hours 6 --output output/my_plan.json
```
JSON file structure:
```json
{
  "total_hours": 6.0,
  "blocks": [
    {
      "index": 1,
      "title": "DS exam",
      "importance": 5,
      "effort_h": 6.0,
      "deadline": "2026-10-30",
      "hours": 6.0
    }
  ],
  "summary": null
}
```

---

## 6. Error Handling & Exit Codes

All errors are handled gracefully without exposing Python tracebacks to end users:

| Exit Code | Condition | Sample Error Output |
| :---: | :--- | :--- |
| `0` | Success | Rendered plan table or confirmation message. |
| `1` | Missing input file | `Error: File not found: samples/missing.csv` |
| `1` | Empty CSV file | `Error: Input CSV file is empty` |
| `1` | Malformed CSV data | `Error: Invalid task row: invalid literal for int() ...` |
| `1` | Invalid study hours | `Error: Study hours must be positive, got: -2` |
| `1` | Infeasible plan | `Error: Infeasible study plan: total mandatory effort exceeds available hours` |

---

## 7. Python Library API

All internal modules can be imported and utilized directly in Python applications:

```python
from datetime import date
from shared.study_planner.parse import parse_csv
from shared.study_planner.prioritise import prioritise
from shared.study_planner.allocate import allocate
from shared.study_planner.render import render
from shared.study_planner.export import export_plan
from shared.study_planner.stats import calculate_stats

# 1. Parse and validate input tasks
tasks = parse_csv("samples/tasks.csv")

# 2. Prioritize tasks
ranked_tasks = prioritise(tasks, today=date(2026, 10, 26))

# 3. Allocate study blocks
blocks = allocate(ranked_tasks, available_hours=8.0)

# 4. Render to terminal
print(render(blocks))

# 5. Export to file
export_plan(blocks, "output/plan.json")

# 6. Aggregate statistics
stats = calculate_stats(blocks)
print(f"Top task: {stats['top_task']}")
```

---

## 8. Team T-W3 Member Roles

| # | Name | Student ID | Role | Target Module | Key Responsibility |
| :---: | :--- | :---: | :--- | :--- | :--- |
| 1 | Nguyễn Phúc Khánh | 25125086 | Tech Lead | `shared/study_planner/__main__.py` | CLI argparse, pipeline integration, merge coordination & release tagging. |
| 2 | Trần Thành Lợi | 25125059 | Developer | `shared/study_planner/export.py` | `export_plan` function exporting JSON / Markdown via `--output`. |
| 3 | Lý Tuấn Kiệt | 25125022 | Presenter, Dev | `shared/study_planner/README.md`, `docs/demo.md` | CLI documentation, sample datasets (`samples/`), presentation & demo guide. |
| 4 | Nguyễn Minh Khang | 25125018 | QA/QC, Presenter | `tests/test_study_planner_e2e.py` | End-to-end test suite and CI maintenance. |
| 5 | Trần Phúc Khánh | 25125020 | Security & Data | `shared/study_planner/errors.py` | Validation, `InfeasiblePlan` handling, clean exit code 1. |
| 6 | Đặng Xuân Phát | 25125062 | UI/UX, QA/QC | `shared/study_planner/stats.py` | Allocation statistics via `Counter` and `defaultdict` (`--stats`). |
