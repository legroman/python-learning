import pytest
import sqlite3

from app.database import create_tasks_table, create_categories_table
from app.database import (
    add_task,
    get_all_tasks,
    get_task_by_id,
    get_tasks_by_status,
    get_tasks_by_title,
    update_task_title,
    update_task_status,
    delete_task,
    count_all_tasks,
    count_tasks_by_done,
    sort_tasks_by_status,
    sort_tasks_by_title,
    delete_completed_tasks,
    add_category,
    get_all_categories,
    get_tasks_with_categories,
    delete_category_by_id,
)


@pytest.fixture
def temp_db(tmp_path, monkeypatch):
    db_file = tmp_path / "test_tasks.db"

    monkeypatch.setattr(
        "app.database.DB_FILE",
        db_file,
    )

    create_categories_table()
    create_tasks_table()

    return db_file


def test_add_task(temp_db):
    add_task("Learn testing")

    tasks = get_all_tasks()

    assert tasks == [(1, "Learn testing", 0, None)]


def test_get_task_by_id(temp_db):
    add_task("Learn testing")

    task = get_task_by_id(1)

    assert task == (1, "Learn testing", 0, None)


def test_get_task_by_invalid_id(temp_db):
    task = get_task_by_id(1)

    assert task is None


def test_update_task_title(temp_db):
    add_task("Learn testing")

    update_task_title(1, "Learn Python")

    task = get_task_by_id(1)

    assert task == (1, "Learn Python", 0, None)


def test_update_task_status(temp_db):
    add_task("Learn testing")

    update_task_status(1, 1)

    task = get_task_by_id(1)

    assert task == (1, "Learn testing", 1, None)


def test_delete_task(temp_db):
    add_task("Learn testing")

    delete_task(1)

    task = get_task_by_id(1)

    assert task is None


def test_get_task_by_status(temp_db):
    add_task("Learn testing")
    add_task("Learn Python", 1)

    tasks = get_tasks_by_status(1)

    assert tasks == [(2, "Learn Python", 1, None)]


def test_get_task_by_title(temp_db):
    add_task("Learn testing")
    add_task("Learn Python")

    tasks = get_tasks_by_title("Python")

    assert tasks == [(2, "Learn Python", 0, None)]


def test_count_all_tasks(temp_db):
    add_task("Learn testing", 1)
    add_task("Learn Python", 1)
    add_task("Buy milk")

    result = count_all_tasks()

    assert result == 3


def test_count_tasks_by_done(temp_db):
    add_task("Learn testing", 1)
    add_task("Learn Python", 1)
    add_task("Buy milk")

    result = count_tasks_by_done(1)

    assert result == 2


def test_sort_tasks_by_title(temp_db):
    add_task("Learn testing")
    add_task("Walk the dog", 1)
    add_task("Buy milk")

    tasks = sort_tasks_by_title()

    assert tasks == [
        (3, "Buy milk", 0, None),
        (1, "Learn testing", 0, None),
        (2, "Walk the dog", 1, None),
    ]


def test_sort_tasks_by_status(temp_db):
    add_task("Learn testing")
    add_task("Walk the dog", 1)
    add_task("Buy milk")
    add_task("Take my brother to school", 1)

    tasks = sort_tasks_by_status()

    assert tasks == [
        (1, "Learn testing", 0, None),
        (3, "Buy milk", 0, None),
        (2, "Walk the dog", 1, None),
        (4, "Take my brother to school", 1, None),
    ]


def test_delete_completed_tasks(temp_db):
    add_task("Learn testing")
    add_task("Walk the dog", 1)
    add_task("Buy milk")
    add_task("Take my brother to school", 1)

    delete_completed_tasks()

    tasks = get_all_tasks()

    assert tasks == [
        (1, "Learn testing", 0, None),
        (3, "Buy milk", 0, None),
    ]


# ================ Categories ==================


def test_add_category(temp_db):
    add_category("Work")
    add_category("Home")

    categories = get_all_categories()

    assert categories == [
        (1, "Work"),
        (2, "Home"),
    ]


def test_add_task_with_category(temp_db):
    add_category("Work")
    add_task("Learn SQL", 0, 1)
    task = get_task_by_id(1)

    assert task == (1, "Learn SQL", 0, 1)


def test_get_tasks_with_categories(temp_db):
    add_category("Work")
    add_category("Home")

    add_task("Learn testing", 0, 1)
    add_task("Walk the dog")
    add_task("Buy milk")
    add_task("Take my brother to school", 0, 2)

    tasks = get_tasks_with_categories()

    assert tasks == [
        (1, "Learn testing", 0, "Work"),
        (2, "Walk the dog", 0, None),
        (3, "Buy milk", 0, None),
        (4, "Take my brother to school", 0, "Home"),
    ]


def test_invalid_foreign_key(temp_db):
    add_category("Work")

    with pytest.raises(sqlite3.IntegrityError):
        add_task("Learn testing", 0, 2)


def test_on_delete_set_null(temp_db):
    add_category("Work")
    add_task("Learn testing", 0, 1)
    delete_category_by_id(1)

    task = get_task_by_id(1)

    assert task == (1, "Learn testing", 0, None)



def test_unique_category(temp_db):
    add_category("Work")

    with pytest.raises(sqlite3.IntegrityError):
        add_category("Work")


def test_check_done_in_task(temp_db):
    with pytest.raises(sqlite3.IntegrityError):
        add_task("Bad task", 7)
