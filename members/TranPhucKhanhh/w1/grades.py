"""W1 grade statistics."""


def summary(scores: list[float]) -> dict[str, float]:
    """Return minimum, maximum, mean, and median for non-empty scores."""
    if len(scores) == 0:
        raise ValueError("Can't enter an empty list")

    max_val = scores[0]
    min_val = scores[0]
    sum = 0
    for val in scores:
        max_val = max(max_val, val)
        min_val = min(min_val, val)
        sum += val

    sorted_list = sorted(scores)

    mean = sum / len(scores)
    median = 0
    if len(scores) % 2 == 0:
        median = (sorted_list[len(scores) // 2] + sorted_list[len(scores) // 2 - 1]) / 2
    else:
        median = sorted_list[len(scores) // 2]

    return {
        "min": min_val,
        "max": max_val,
        "mean": round(mean, 2),
        "median": round(median, 2),
    }
