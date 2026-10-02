from task_manager import is_valid_task
from task_manager import clear_completed


def test_valid_task():
    task = {"title": "Learn pytest", "done": False}

    assert is_valid_task(task) is True


def test_invalid_task():
    task = {"title": "Learn pytest"}

    assert is_valid_task(task) is False


def test_invalid_done_type():
    task = {"title": "Learn pytest", "done": "no"}

    assert is_valid_task(task) is False


def test_invalid_title_type():
    task = {"title": 123, "done": False}

    assert is_valid_task(task) is False


def test_invalid_task_type():
    task = "Learn pytest"

    assert is_valid_task(task) is False


def test_clear_completed(monkeypatch):
    tasks = [
        {"title": "Task 1", "done": True},
        {"title": "Task 2", "done": False},
    ]

    monkeypatch.setattr("builtins.input", lambda _: "yes")

    clear_completed(tasks)

    assert tasks == [
        {"title": "Task 2", "done": False},
    ]


def test_clear_completed_cancelled(monkeypatch):
    tasks = [
        {"title": "Task 1", "done": True},
        {"title": "Task 2", "done": False},
    ]

    monkeypatch.setattr("builtins.input", lambda _: "no")

    clear_completed(tasks)

    assert tasks == [
        {"title": "Task 1", "done": True},
        {"title": "Task 2", "done": False},
    ]