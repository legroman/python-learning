from models import is_valid_task
from task_manager import clear_completed
from task_manager import load_tasks
from task_manager import save_tasks
import json
import pytest


@pytest.fixture
def temp_dir(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    return tmp_path


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


def test_load_tasks(temp_dir):
    file_path = temp_dir / "tasks.json"
    file_path.write_text(
        '[{"title": "Learn pytest", "done": false}]',
        encoding="utf-8",
    )

    tasks = load_tasks()

    assert tasks == [
        {"title": "Learn pytest", "done": False},
    ]


def test_load_tasks_missing_file(temp_dir):
    tasks = load_tasks()

    assert tasks == []


def test_load_tasks_invalid_json(temp_dir):
    file_path = temp_dir / "tasks.json"
    file_path.write_text("not valid json", encoding="utf-8")

    tasks = load_tasks()

    assert tasks == []


def test_load_tasks_not_list(temp_dir):
    file_path = temp_dir / "tasks.json"
    file_path.write_text(
        '{"title": "Learn pytest", "done": false}',
        encoding="utf-8",
    )

    tasks = load_tasks()

    assert tasks == []


def test_load_tasks_filters_invalid_tasks(temp_dir):
    file_path = temp_dir / "tasks.json"
    file_path.write_text(
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


def test_save_tasks(temp_dir):
    tasks = [
        {"title": "Learn pytest", "done": False},
        {"title": "Learn Git", "done": True},
    ]

    save_tasks(tasks)

    file_path = temp_dir / "tasks.json"

    assert file_path.exists()

    saved_tasks = json.loads(file_path.read_text(encoding="utf-8"))

    assert saved_tasks == tasks
