import json
import logging
from app.models import Task, is_valid_task
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
TASKS_FILE = BASE_DIR / "tasks.json"

logger = logging.getLogger(__name__)


def load_tasks() -> list[Task]:
    try:
        with open(TASKS_FILE, "r", encoding="utf-8") as file:
            raw_tasks = json.load(file)
            if not isinstance(raw_tasks, list):
                return []
            logger.info("Tasks loaded successfully")
            return [task for task in raw_tasks if is_valid_task(task)]
    except (FileNotFoundError, json.JSONDecodeError):
        logger.warning("Could not load tasks")
        return []


def save_tasks(tasks: list[Task]) -> bool:
    try:
        with open(TASKS_FILE, "w", encoding="utf-8") as file:
            json.dump(tasks, file, indent=4, ensure_ascii=False)
            logger.info("Tasks saved successfully")
        return True
    except OSError:
        logger.exception("Could not save tasks")
        return False