from members.khanh_np.w2.models import Task


class InfeasiblePlan(Exception):
    def __init__(self, needed_h: float, available_h: float) -> None:
        super().__init__(f"Infeasible plan: needed {needed_h}h exceeds available {available_h}h")
        self.needed_h = needed_h
        self.available_h = available_h


# Alias to satisfy both test_w2.py and AGENTS.md conventions
InfeasiblePlanError = InfeasiblePlan


def check_feasible(tasks: list[Task], available_h: float) -> None:
    needed_h = sum(t.effort_h for t in tasks)
    if needed_h > available_h:
        raise InfeasiblePlan(needed_h, available_h)
