import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_FILE = BASE_DIR / "tasks.db"


def get_connection() -> sqlite3.Connection:
    return sqlite3.connect(DB_FILE)


def create_tasks_table() -> None:
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            done INTEGER NOT NULL
        )
        """)

    connection.close()


def add_task(title: str, done: int = 0) -> None:
    connection = get_connection()

    connection.execute(
        """
        INSERT INTO tasks (title, done)
        VALUES (?, ?)
        """,
        (title, done),
    )

    connection.commit()
    connection.close()


def get_all_tasks() -> list[tuple[int, str, int]]:
    connection = get_connection()

    tasks = connection.execute("SELECT * FROM tasks").fetchall()
    connection.close()

    return tasks


def get_task_by_id(task_id: int) -> tuple[int, str, int] | None:
    connection = get_connection()

    task = connection.execute(
        """
            SELECT * FROM tasks
            WHERE id = ?
            """,
        (task_id,),
    ).fetchone()

    connection.close()

    return task


def update_task_title(task_id: int, new_title: str) -> None:
    connection = get_connection()

    connection.execute(
        """
        UPDATE tasks
        SET title = ?
        WHERE id = ?
        """,
        (new_title, task_id),
    )

    connection.commit()
    connection.close()


def delete_task(task_id: int) -> None:
    connection = get_connection()

    connection.execute(
        """
        DELETE FROM tasks
        WHERE id = ?
        """,
        (task_id,),
    )

    connection.commit()
    connection.close()


def update_task_status(task_id: int, done: int) -> None:
    connection = get_connection()

    connection.execute(
        """
        UPDATE tasks
        SET done = ?
        WHERE id = ?
        """,
        (done, task_id),
    )

    connection.commit()
    connection.close()


def get_tasks_by_status(done: int) -> list[tuple[int, str, int]]:
    connection = get_connection()

    tasks = connection.execute(
        """
        SELECT * FROM tasks
        WHERE done = ?
        """,
        (done,),
    ).fetchall()

    connection.close()

    return tasks


def get_tasks_by_title(title: str) -> list[tuple[int, str, int]]:
    connection = get_connection()

    tasks = connection.execute(
        """
        SELECT * FROM tasks
        WHERE title LIKE ?
        """,
        (f"%{title}%",),
    ).fetchall()

    connection.close()

    return tasks


def count_tasks_by_done(done: int) -> int:
    connection = get_connection()

    result = connection.execute(
        """
        SELECT COUNT(*)
        FROM tasks
        WHERE done = ?
        """,
        (done,),
    ).fetchone()

    connection.close()

    return result[0] if result is not None else 0


def count_all_tasks() -> int:
    connection = get_connection()

    result = connection.execute(
        """
        SELECT COUNT(*) FROM tasks
        """,
    ).fetchone()

    connection.close()

    return result[0] if result is not None else 0


def sort_tasks_by_status() -> list[tuple[int, str, int]]:
    connection = get_connection()

    result = connection.execute(
        """
        SELECT * FROM tasks
        ORDER BY done ASC
        """,
    ).fetchall()

    connection.close()

    return result


def sort_tasks_by_title() -> list[tuple[int, str, int]]:
    connection = get_connection()

    result = connection.execute(
        """
        SELECT * FROM tasks
        ORDER BY title ASC
        """,
    ).fetchall()

    connection.close()

    return result


def delete_completed_tasks() -> None:
    connection = get_connection()

    connection.execute(
        """
        DELETE FROM tasks
        WHERE done = 1
        """,
    )

    connection.commit()
    connection.close()


def get_completed_tasks() -> list[tuple[int, str]]:
    connection = get_connection()

    result = connection.execute(
        """
        SELECT id, title FROM tasks
        WHERE done = 1
        ORDER BY title ASC
        """,
    ).fetchall()

    connection.close()

    return result

