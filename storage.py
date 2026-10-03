import json
from models import Task, is_valid_task


def load_tasks() -> list[Task]:
    try:
        with open("tasks.json", "r", encoding="utf-8") as file:
            raw_tasks = json.load(file)
            if not isinstance(raw_tasks, list):
                return []
            return [task for task in raw_tasks if is_valid_task(task)]
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_tasks(tasks: list[Task]) -> None:
    with open("tasks.json", "w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=4, ensure_ascii=False)
