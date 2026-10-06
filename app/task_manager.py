from app.database import add_task as add_task_to_db
from app.database import get_all_tasks
from app.database import get_task_by_id
from app.database import delete_task as delete_task_from_db
from app.database import delete_completed_tasks
from app.database import update_task_title, update_task_status
from app.database import get_tasks_by_status, get_tasks_by_title
from app.database import count_all_tasks, count_tasks_by_done
from app.database import sort_tasks_by_status, sort_tasks_by_title


def show_menu() -> None:
    print("\nTask Manager")
    print("1. Add task")
    print("2. Show tasks")
    print("3. Toggle task")
    print("4. Delete task")
    print("5. Edit task")
    print("6. Filter tasks")
    print("7. Search tasks")
    print("8. Show statistics")
    print("9. Sort tasks")
    print("10. Clear completed")
    print("11. Exit")


def show_tasks(_tasks=None) -> None:
    tasks = get_all_tasks() if _tasks is None else _tasks

    if not tasks:
        print("No tasks yet.")
    else:
        for task in tasks:
            status = "✓" if task[2] else " "
            print(f"{task[0]}. [{status}] {task[1]}")


def add_task() -> None:
    task = input("Enter task: ").strip()
    if not task:
        print("Task cannot be empty.")
    else:
        add_task_to_db(task)
        print("Task added!")



def toggle_task() -> None:
    try:
        task_id = int(input("Enter task id: "))
    except ValueError:
        print("Invalid task id.")
        return

    task = get_task_by_id(task_id)

    if task is None:
        print("No such task.")
        return

    new_status = 0 if task[2] else 1

    update_task_status(task_id, new_status)

    status = "completed" if new_status else "not completed"
    print(f"Task marked as {status}")


def delete_task() -> None:
    try:
        task_id = int(input("Enter task id: "))
    except ValueError:
        print("Invalid task id.")
        return

    task = get_task_by_id(task_id)

    if task is None:
        print("No such task.")
        return

    delete_task_from_db(task_id)

    print(f"Task '{task[1]}' was deleted")


def edit_task() -> None:
    try:
        task_id = int(input("Enter task id: "))
    except ValueError:
        print("Invalid task id.")
        return

    task = get_task_by_id(task_id)

    if task is None:
        print("No such task.")
        return

    new_task = input("Enter a new task: ").strip()

    if not new_task:
        print("Task cannot be empty")
        return

    update_task_title(task_id, new_task)
    print("Task was edited")


def filter_tasks() -> None:
    print("1. All")
    print("2. Active")
    print("3. Completed")

    choice = input("Choose an option: ")

    if choice == "1":
        show_tasks()
    elif choice == "2":
        active_tasks = get_tasks_by_status(0)
        show_tasks(active_tasks)
    elif choice == "3":
        completed_tasks = get_tasks_by_status(1)
        show_tasks(completed_tasks)
    else:
        print("Invalid option.")


def search_tasks() -> None:
    search_text = input("Enter search text: ").strip()
    if not search_text:
        print("Search text cannot be empty.")
        return
    tasks_found = get_tasks_by_title(search_text)
    show_tasks(tasks_found)


def show_statistics() -> None:
    total = count_all_tasks()
    completed = count_tasks_by_done(1)
    active = total - completed

    print(f"Total: {total}")
    print(f"Completed: {completed}")
    print(f"Active: {active}")


def sort_tasks() -> None:
    print("1. By status")
    print("2. By title")

    choice = input("Choose sort type: ")

    if choice == "1":
        tasks = sort_tasks_by_status()
        show_tasks(tasks)
    elif choice == "2":
        tasks = sort_tasks_by_title()
        show_tasks(tasks)
    else:
        print("Invalid option.")


def clear_completed() -> None:
    print("Are you sure?")
    choice = input("Enter yes to confirm: ").strip().lower()

    if choice == "yes":
        delete_completed_tasks()
        print("Completed tasks cleared.")
    else:
        print("Clear cancelled.")


def main() -> None:
    while True:
        show_menu()

        choice = input("Choose an option: ")

        if choice == "11":
            print("Goodbye!")
            break
        elif choice == "1":
            add_task()
        elif choice == "2":
            show_tasks()
        elif choice == "3":
            toggle_task()
        elif choice == "4":
            delete_task()
        elif choice == "5":
            edit_task()
        elif choice == "6":
            filter_tasks()
        elif choice == "7":
            search_tasks()
        elif choice == "8":
            show_statistics()
        elif choice == "9":
            sort_tasks()
        elif choice == "10":
            clear_completed()
        else:
            print("Invalid option")
