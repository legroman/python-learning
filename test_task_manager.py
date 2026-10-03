import json

import pytest

from app.models import is_valid_task
from app.storage import load_tasks, save_tasks
from app.task_manager import clear_completed


@pytest.fixture
def temp_file_path(tmp_path, monkeypatch):
    file_path = tmp_path / "tasks.json"

    monkeypatch.setattr(
        "app.storage.TASKS_FILE",
        file_path,
    )

    return file_path


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


def test_load_tasks(temp_file_path):
    temp_file_path.write_text(
        '[{"title": "Learn pytest", "done": false}]',
        encoding="utf-8",
    )

    tasks = load_tasks()

    assert tasks == [
        {"title": "Learn pytest", "done": False},
    ]


def test_load_tasks_missing_file(temp_file_path):
    tasks = load_tasks()

    assert tasks == []


def test_load_tasks_invalid_json(temp_file_path):
    temp_file_path.write_text("not valid json", encoding="utf-8")

    tasks = load_tasks()

    assert tasks == []


def test_load_tasks_not_list(temp_file_path):
    temp_file_path.write_text(
        '{"title": "Learn pytest", "done": false}',
        encoding="utf-8",
    )

    tasks = load_tasks()

    assert tasks == []


def test_load_tasks_filters_invalid_tasks(temp_file_path):
    temp_file_path.write_text(
        """
        [
            {"title": "Valid task", "done": false},
            {"title": "Missing done"},
            {"title": 123, "done": true},
            "not a task"
        ]
        """,
        encoding="utf-8",
    )

    tasks = load_tasks()

    assert tasks == [
        {"title": "Valid task", "done": False},
    ]


def test_save_tasks(temp_file_path):
    tasks = [
        {"title": "Learn pytest", "done": False},
        {"title": "Learn Git", "done": True},
    ]

    save_tasks(tasks)

    assert temp_file_path.exists()

    saved_tasks = json.loads(temp_file_path.read_text(encoding="utf-8"))

    assert saved_tasks == tasks
