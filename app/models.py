from typing import TypedDict, TypeGuard

class Task(TypedDict):
    title: str
    done: bool


def is_valid_task(task: object) -> TypeGuard[Task]:
    return (
        isinstance(task, dict)
        and "title" in task
        and isinstance(task["title"], str)
        and "done" in task
        and isinstance(task["done"], bool)
    )