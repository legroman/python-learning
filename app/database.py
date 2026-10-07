import sqlite3
from pathlib import Path
from contextlib import closing

BASE_DIR = Path(__file__).resolve().parent.parent
DB_FILE = BASE_DIR / "tasks.db"


def get_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(DB_FILE)
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def create_tasks_table() -> None:
    with closing(get_connection()) as connection:

        connection.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                done INTEGER NOT NULL CHECK (done IN (0, 1)),
                category_id INTEGER,
                FOREIGN KEY (category_id)
                REFERENCES categories(id)
                ON DELETE SET NULL
            )
            """)

        connection.execute("""
            CREATE INDEX IF NOT EXISTS idx_tasks_category_id
            ON tasks(category_id)
            """)


def create_categories_table() -> None:
    with closing(get_connection()) as connection:

        connection.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL UNIQUE
            )
            """)


def add_task(title: str, done: int = 0, category_id: int | None = None) -> None:
    with closing(get_connection()) as connection:
        with connection:
            connection.execute(
                """
                INSERT INTO tasks (title, done, category_id)
                VALUES (?, ?, ?)
                """,
                (title, done, category_id),
            )


def get_all_tasks() -> list[tuple[int, str, int]]:
    with closing(get_connection()) as connection:
        tasks = connection.execute("SELECT * FROM tasks").fetchall()

    return tasks


def get_task_by_id(task_id: int) -> tuple[int, str, int] | None:
    with closing(get_connection()) as connection:
        task = connection.execute(
            """
                SELECT * FROM tasks
                WHERE id = ?
                """,
            (task_id,),
        ).fetchone()

    return task


def update_task_title(task_id: int, new_title: str) -> None:
    with closing(get_connection()) as connection:
        with connection:
            connection.execute(
                """
                UPDATE tasks
                SET title = ?
                WHERE id = ?
                """,
                (new_title, task_id),
            )


def delete_task(task_id: int) -> None:
    with closing(get_connection()) as connection:
        with connection:
            connection.execute(
                """
                DELETE FROM tasks
                WHERE id = ?
                """,
                (task_id,),
            )


def update_task_status(task_id: int, done: int) -> None:
    with closing(get_connection()) as connection:
        with connection:
            connection.execute(
                """
                UPDATE tasks
                SET done = ?
                WHERE id = ?
                """,
                (done, task_id),
            )


def get_tasks_by_status(done: int) -> list[tuple[int, str, int]]:
    with closing(get_connection()) as connection:
        tasks = connection.execute(
            """
            SELECT * FROM tasks
            WHERE done = ?
            """,
            (done,),
        ).fetchall()

    return tasks


def get_tasks_by_title(title: str) -> list[tuple[int, str, int]]:
    with closing(get_connection()) as connection:
        tasks = connection.execute(
            """
            SELECT * FROM tasks
            WHERE title LIKE ?
            """,
            (f"%{title}%",),
        ).fetchall()

    return tasks


def count_tasks_by_done(done: int) -> int:
    with closing(get_connection()) as connection:
        result = connection.execute(
            """
            SELECT COUNT(*)
            FROM tasks
            WHERE done = ?
            """,
            (done,),
        ).fetchone()

    return result[0] if result is not None else 0


def count_all_tasks() -> int:
    with closing(get_connection()) as connection:
        result = connection.execute(
            """
            SELECT COUNT(*) FROM tasks
            """,
        ).fetchone()

    return result[0] if result is not None else 0


def sort_tasks_by_status() -> list[tuple[int, str, int]]:
    with closing(get_connection()) as connection:
        result = connection.execute(
            """
            SELECT * FROM tasks
            ORDER BY done ASC
            """,
        ).fetchall()

    return result


def sort_tasks_by_title() -> list[tuple[int, str, int]]:
    with closing(get_connection()) as connection:
        result = connection.execute(
            """
            SELECT * FROM tasks
            ORDER BY title ASC
            """,
        ).fetchall()

    return result


def delete_completed_tasks() -> None:
    with closing(get_connection()) as connection:
        with connection:
            connection.execute(
                """
                DELETE FROM tasks
                WHERE done = 1
                """,
            )


def get_completed_tasks() -> list[tuple[int, str]]:
    with closing(get_connection()) as connection:
        result = connection.execute(
            """
            SELECT id, title FROM tasks
            WHERE done = 1
            ORDER BY title ASC
            """,
        ).fetchall()

    return result


# ================ Categories ==================


def add_category(name: str) -> None:
    with closing(get_connection()) as connection:
        with connection:
            connection.execute(
                """
                INSERT INTO categories (name)
                VALUES (?)
                """,
                (name,),
            )


def get_all_categories() -> list[tuple[int, str]]:
    with closing(get_connection()) as connection:
        result = connection.execute(
            """
            SELECT * FROM categories
            """,
        ).fetchall()

    return result


def get_tasks_with_categories() -> list[tuple[int, str, int, str | None]]:
    with closing(get_connection()) as connection:
        result = connection.execute(
            """
            SELECT tasks.id, tasks.title, tasks.done, categories.name 
            FROM tasks
            LEFT JOIN categories
            ON tasks.category_id = categories.id
            """,
        ).fetchall()

    return result


def delete_category_by_id(category_id: int) -> None:
    with closing(get_connection()) as connection:
        with connection:
            connection.execute(
                """
                DELETE FROM categories
                WHERE id = ?
                """,
                (category_id,),
            )


def migrate_tasks_add_category() -> None:
    with closing(get_connection()) as connection:
        with connection:
            connection.execute("""
                CREATE TABLE tasks_new (
                    id INTEGER PRIMARY KEY,
                    title TEXT NOT NULL,
                    done INTEGER NOT NULL CHECK (done IN (0, 1)),
                    category_id INTEGER,
                    FOREIGN KEY (category_id)
                    REFERENCES categories(id)
                    ON DELETE SET NULL
                )
                """)

            connection.execute("""
                INSERT INTO tasks_new (id, title, done)
                SELECT id, title, done
                FROM tasks
                """)

            connection.execute("""DROP TABLE tasks""")

            connection.execute("""ALTER TABLE tasks_new RENAME TO tasks""")

            connection.execute("""
            CREATE INDEX IF NOT EXISTS idx_tasks_category_id
            ON tasks(category_id)
            """)
