# Study Planner CLI — Live Demo & Presentation Guide (Team T-W3)

- **Project**: Study Planner CLI Integration
- **Team**: Team T-W3 (Team 07)
- **Presenter**: Lý Tuấn Kiệt (Student ID: 25125022 — GitHub: `@kiethm07`)
- **Reference Documentation**: [shared/study_planner/README.md](../shared/study_planner/README.md)

---

## 1. Presentation Objectives

1. Demonstrate modular software architecture and continuous integration (CI/CD) practices.
2. Deliver a live terminal demo of the `shared.study_planner` command-line application.
3. Highlight core features:
   - Greedy allocation and urgency-based prioritization.
   - Deep statistical analysis using `Counter` and `defaultdict` (`--stats`).
   - Multi-format file export to Markdown and JSON (`--output`).
   - Robust error handling that exits cleanly without exposing Python tracebacks.

---

## 2. Presentation Agenda & Time Allocation (15 Minutes)

| Section | Duration | Key Topics | Presenter Activity |
| :---: | :---: | :--- | :--- |
| **Part 1** | 2 mins | Team introduction, role breakdown, and project goals. | Slides 1 – 2 |
| **Part 2** | 3 mins | Pipeline architecture, data contracts (`Task`, `Block`), and integration flow. | Slides 3 – 4 |
| **Part 3** | 6 mins | **Live Terminal Demo**: Executing 5 real-world usage scenarios. | Live Terminal |
| **Part 4** | 2 mins | Quality Assurance (QA/QC): E2E test suite coverage and CI linting. | Slide 5 |
| **Part 5** | 2 mins | Conclusion and Question & Answer (Q&A). | Slide 6 |

---

## 3. Step-by-Step Live Demo Script

> **Presenter Tip**: Open terminal in the repository root directory `python-bootcamp`.

### Preparation
```bash
# Verify environment and sample files
git status
ls samples/
```

---

### Scenario 1: Basic Study Allocation (Greedy Scheduling)
- **Objective**: Demonstrate CSV parsing, task prioritization, and greedy hour allocation.
- **Presenter Script**: *"First, we execute the planner on `samples/tasks.csv` with 8 available study hours."*
- **Command**:
  ```bash
  python -m shared.study_planner samples/tasks.csv --hours 8
  ```
- **Talking Points**:
  - The high-priority task `DS exam` (`importance=5`) is scheduled first with its full 6.0 hours.
  - The remaining 1.5 hours are allocated to `Assignment`.
  - Total allocated hours: 7.5h / 8.0h available.

---

### Scenario 2: Realistic Dataset & Reference Date (`--today`)
- **Objective**: Test with the extended dataset (`samples/tasks_extended.csv`) containing 7 subjects, varied priorities (1–5), and distinct deadlines.
- **Presenter Script**: *"Using our extended dataset, we can provide a custom reference date `--today` to calculate urgency dynamically relative to that date."*
- **Command**:
  ```bash
  python -m shared.study_planner samples/tasks_extended.csv --hours 12 --today 2026-10-28
  ```
- **Talking Points**:
  - Tasks closest to `2026-10-28` with `importance=5` take precedence.
  - Tasks with distant deadlines or lower ratings are deprioritized or trimmed once hours are exhausted.

---

### Scenario 3: Allocation Statistics (`--stats`)
- **Objective**: Showcase metrics aggregation powered by `collections.Counter` and `collections.defaultdict`.
- **Presenter Script**: *"When students need insight into how their study time is distributed, the `--stats` flag aggregates total hours and percentage share by importance level."*
- **Command**:
  ```bash
  python -m shared.study_planner samples/tasks_extended.csv --hours 10 --stats
  ```
- **Observed Output**:
  - Identifies the Top Task consuming the most study time.
  - Percentage and block count breakdown across importance levels 5 down to 1.

---

### Scenario 4: Exporting Plan to Markdown & JSON (`--output`)
- **Objective**: Demonstrate interoperability with external note-taking tools and data services.
- **Presenter Script**: *"Study schedules can be directly exported to Markdown for personal notes (e.g., Notion/Obsidian) or JSON for external API consumption."*
- **Command**:
  ```bash
  # 1. Export to Markdown table
  python -m shared.study_planner samples/tasks_extended.csv --hours 8 --output output/demo_plan.md

  # 2. Export to structured JSON
  python -m shared.study_planner samples/tasks_extended.csv --hours 8 --output output/demo_plan.json
  ```
- **Verify Exported Content**:
  ```bash
  head -n 20 output/demo_plan.md
  head -n 25 output/demo_plan.json
  ```

---

### Scenario 5: Graceful Error Handling
- **Objective**: Verify that user input errors fail gracefully with exit code `1` and clean messages without tracebacks.
- **Presenter Script**: *"Robust input validation guarantees an intuitive user experience even under improper usage."*

1. **Missing Input File**:
   ```bash
   python -m shared.study_planner samples/nonexistent.csv --hours 4
   # Expected: Clean file-not-found error message, exit code 1
   ```
2. **Malformed CSV Data (`tasks_bad.csv`)**:
   ```bash
   python -m shared.study_planner samples/tasks_bad.csv --hours 4
   # Expected: Clear row parsing error without stack trace
   ```
3. **Invalid Study Hours**:
   ```bash
   python -m shared.study_planner samples/tasks.csv --hours -5
   # Expected: Non-zero exit code with positive hours constraint message
   ```

---

### Scenario 6: Automated End-to-End Testing & Code Quality
- **Objective**: Confirm software stability through automated test suites and linting.
- **Commands**:
  ```bash
  # Run End-to-End integration test suite
  pytest -q tests/test_study_planner_e2e.py

  # Run code quality linter
  ruff check shared/study_planner
  ```

---

## 4. Q&A Defense & Anticipated Questions

### Question 1: Why did the team choose a Greedy approach for `allocate`?
- **Answer**: The allocation problem naturally maps to the Fractional Knapsack model where items are ranked by benefit-to-weight ratio. Greedy allocation runs in $\mathcal{O}(N \log N)$ time (dominated by sorting), making it fast, deterministic, and intuitive for users.

### Question 2: How did component modularity benefit team collaboration?
- **Answer**: Each member worked against shared data contracts (`shared.contract.Task`, `Block`). This decoupled development and testing, allowing all 6 members to build and test their modules concurrently without merge conflicts before final CLI assembly in `__main__.py`.

### Question 3: How are overdue deadlines handled when `--today` is past the deadline?
- **Answer**: The `prioritise` module computes `days_left`. When `days_left < 0`, the task is marked as overdue and flagged in the summary report so students can urgently address backlog tasks.
