from task_manager import is_valid_task
from task_manager import clear_completed
from task_manager import load_tasks
from task_manager import save_tasks
import json


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


def test_load_tasks(tmp_path, monkeypatch):
    file_path = tmp_path / "tasks.json"
    file_path.write_text(
        '[{"title": "Learn pytest", "done": false}]',
        encoding="utf-8",
    )

    monkeypatch.chdir(tmp_path)

    tasks = load_tasks()

    assert tasks == [
        {"title": "Learn pytest", "done": False},
    ]


def test_load_tasks_missing_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    tasks = load_tasks()

    assert tasks == []


def test_load_tasks_invalid_json(tmp_path, monkeypatch):
    file_path = tmp_path / "tasks.json"
    file_path.write_text("not valid json", encoding="utf-8")

    monkeypatch.chdir(tmp_path)

    tasks = load_tasks()

    assert tasks == []


def test_load_tasks_not_list(tmp_path, monkeypatch):
    file_path = tmp_path / "tasks.json"
    file_path.write_text(
        '{"title": "Learn pytest", "done": false}',
        encoding="utf-8",
    )

    monkeypatch.chdir(tmp_path)

    tasks = load_tasks()

    assert tasks == []


def test_load_tasks_filters_invalid_tasks(tmp_path, monkeypatch):
    file_path = tmp_path / "tasks.json"
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

    monkeypatch.chdir(tmp_path)

    tasks = load_tasks()

    assert tasks == [
        {"title": "Valid task", "done": False},
    ]


def test_save_tasks(tmp_path, monkeypatch):
    tasks = [
        {"title": "Learn pytest", "done": False},
        {"title": "Learn Git", "done": True},
    ]

    monkeypatch.chdir(tmp_path)

    save_tasks(tasks)

    file_path = tmp_path / "tasks.json"

    assert file_path.exists()

    saved_tasks = json.loads(file_path.read_text(encoding="utf-8"))

    assert saved_tasks == tasks
