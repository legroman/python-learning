import json
from app.models import Task, is_valid_task
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
TASKS_FILE = BASE_DIR / "tasks.json"


def load_tasks() -> list[Task]:
    try:
        with open(TASKS_FILE, "r", encoding="utf-8") as file:
            raw_tasks = json.load(file)
            if not isinstance(raw_tasks, list):
                return []
            return [task for task in raw_tasks if is_valid_task(task)]
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_tasks(tasks: list[Task]) -> None:
    with open(TASKS_FILE, "w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=4, ensure_ascii=False)
