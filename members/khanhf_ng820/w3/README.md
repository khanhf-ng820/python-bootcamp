# Week 3 Exercises — khanhf_ng820

## Modules
- `dates.py`: Natural date parser (`parse_due`) supporting ISO dates, 'tomorrow', 'in N days', and weekday names.
- `log_stats.py`: Latency statistics analyzer (`analyse`) returning request counts, p95 latencies, and slowest endpoint.
- `cli.py`: Interactive study planner CLI accepting `--hours` and `--today`.

## Python vs C++ Reflection (W3-4)
1. Dynamic typing and duck typing make standard library collections (e.g. `Counter`, `defaultdict`) far more concise than C++ `std::unordered_map` without needing verbose template instantiations or custom hashers.
2. Expressive date arithmetic with `datetime` and `timedelta` avoids the boilerplate and complex duration conversions of C++ `<chrono>`.
3. Built-in list/dict comprehensions and generator expressions make data transformation pipelines much shorter and more readable than C++ `<algorithm>` iterator loops.
