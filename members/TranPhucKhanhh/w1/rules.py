"""W1 thesis eligibility checks."""


def can_register_thesis(credits: int, gpa: float) -> bool:
    """Check whether both thesis registration requirements are satisfied."""
    return credits >= 120 and gpa >= 2.0


def missing(credits: int, gpa: float) -> list[str]:
    """List the credit and GPA requirements that remain unsatisfied."""
    if can_register_thesis(credits, gpa):
        return []
    else:
        miss = []
        if credits < 120:
            miss.append(f"need {120 - credits} more credits")
        if gpa < 2.0:
            miss.append(f"GPA is missing {2.0 - gpa}")

    return miss
