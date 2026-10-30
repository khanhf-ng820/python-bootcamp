# Week 3 Exercises — kiethm07 (Lý Tuấn Kiệt)

## Modules Overview
- `dates.py`: Deadline and relative date expression parser (`parse_due`) supporting ISO 8601 strings, `'today'`, `'tomorrow'`, `'in N days'`, and upcoming weekday occurrences.
- `log_stats.py`: Microservice latency and endpoint analyzer (`analyse`) returning request counts, nearest-rank 95th percentile (p95) latencies, and identifying the slowest route.
- `cli.py`: Command-line interface study planner application consuming CSV tasks, prioritizing urgency relative to `--today`, and allocating study hours with clean error exits (`sys.exit(1)`).

---

## Python vs C++ Reflection (W3-4)

1. **Dynamic Typing & Duck Typing vs Compile-Time Templates**:
   Python functions dynamically accept any iterable or structure adhering to protocol interfaces without verbose static template declarations, traits, or complex compile-time constraints required in C++.
2. **Standard Collections & Comprehensions**:
   High-level abstractions like `collections.Counter`, `collections.defaultdict`, and native dictionary/list comprehensions eliminate manual map initialization loops and boilerplate standard iterator loops in C++ (`std::unordered_map` / `<algorithm>`).
3. **Date & Time Arithmetic**:
   Standard library `datetime.date` and `datetime.timedelta` allow intuitive calendar calculations without dealing with duration ratios, clock types, and duration conversions of C++ `<chrono>`.
