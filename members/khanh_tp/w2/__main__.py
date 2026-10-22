"""W2-5: Run with python -m members.khanh_tp.w2."""
from pathlib import Path

from .io_utils import load_tasks


def main() -> None:
    path = Path(__file__).resolve().parents[3] / "samples" / "tasks.csv"
    for task in load_tasks(path):
        print(task)


if __name__ == "__main__":
    main()
