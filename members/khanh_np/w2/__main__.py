import sys
from pathlib import Path

from members.khanh_np.w2.io_utils import load_tasks


def main() -> None:
    if len(sys.argv) > 1:
        csv_path = Path(sys.argv[1])
    else:
        csv_path = Path(__file__).resolve().parents[3] / "samples" / "tasks.csv"

    tasks = load_tasks(csv_path)
    for task in tasks:
        print(f"- {task.title} (importance={task.importance}, effort={task.effort_h}h, deadline={task.deadline})")


if __name__ == "__main__":
    main()
