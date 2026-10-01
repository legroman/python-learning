import json


def is_valid_task(task):
    return (
        isinstance(task, dict)
        and "title" in task
        and isinstance(task["title"], str)
        and "done" in task
        and isinstance(task["done"], bool)
    )


def load_tasks():
    try:
        with open("tasks.json", "r", encoding="utf-8") as file:
            raw_tasks = json.load(file)
            if not isinstance(raw_tasks, list):
                return []
            return [task for task in raw_tasks if is_valid_task(task)]
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_tasks(tasks):
    with open("tasks.json", "w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=4, ensure_ascii=False)


def show_menu():
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
    print("10. Exit")


def show_tasks(tasks):
    if not tasks:
        print("No tasks yet.")
    else:
        for index, task in enumerate(tasks, start=1):
            status = "✓" if task["done"] else " "
            print(f"{index}. [{status}] {task['title']}")


def add_task(tasks):
    task = input("Enter task: ").strip()
    if not task:
        print("Task cannot be empty.")
    else:
        tasks.append({"title": task, "done": False})
        save_tasks(tasks)
        print("Task added!")


def get_task_number(tasks):
    try:
        task_number = int(input("Enter task number: "))
        if 0 < task_number <= len(tasks):
            return task_number
        print("No such task number.")
        return None
    except ValueError:
        print("Invalid task number.")
        return None


def toggle_task(tasks):
    task_number = get_task_number(tasks)
    if task_number:
        task = tasks[task_number - 1]
        task["done"] = not task["done"]
        save_tasks(tasks)
        status = "completed" if task["done"] else "not completed"
        print(f"Task marked as {status}")


def delete_task(tasks):
    task_number = get_task_number(tasks)
    if task_number:
        removed_task = tasks.pop(task_number - 1)
        save_tasks(tasks)
        print(f"Task [{removed_task['title']}] was deleted")


def edit_task(tasks):
    task_number = get_task_number(tasks)
    if task_number:
        new_task = input("Enter a new task: ").strip()
        if not new_task:
            print("Task cannot be empty")
        else:
            tasks[task_number - 1]["title"] = new_task
            save_tasks(tasks)
            print("Task was edited")


def filter_tasks(tasks):
    print("1. All")
    print("2. Active")
    print("3. Completed")

    choice = input("Choose an option: ")

    if choice == "1":
        show_tasks(tasks)
    elif choice == "2":
        active_tasks = [task for task in tasks if not task["done"]]
        show_tasks(active_tasks)
    elif choice == "3":
        completed_tasks = [task for task in tasks if task["done"]]
        show_tasks(completed_tasks)
    else:
        print("Invalid option.")


def search_tasks(tasks):
    search_text = input("Enter search text: ").strip().lower()
    if not search_text:
        print("Search text cannot be empty.")
        return
    tasks_found = [task for task in tasks if search_text in task["title"].lower()]
    show_tasks(tasks_found)


def show_statistics(tasks):
    total = len(tasks)
    completed = sum(task["done"] for task in tasks)
    active = total - completed

    print(f"Total: {total}")
    print(f"Completed: {completed}")
    print(f"Active: {active}")


def sort_tasks(tasks):
    tasks.sort(key=lambda task: task["done"])
    save_tasks(tasks)
    print("Task sorted.")


def main():
    tasks = load_tasks()

    while True:
        show_menu()

        choice = input("Choose an option: ")

        if choice == "10":
            print("Goodbye!")
            break
        elif choice == "1":
            add_task(tasks)
        elif choice == "2":
            show_tasks(tasks)
        elif choice == "3":
            toggle_task(tasks)
        elif choice == "4":
            delete_task(tasks)
        elif choice == "5":
            edit_task(tasks)
        elif choice == "6":
            filter_tasks(tasks)
        elif choice == "7":
            search_tasks(tasks)
        elif choice == "8":
            show_statistics(tasks)
        elif choice == "9":
            sort_tasks(tasks)
        else:
            print("Invalid option")


if __name__ == "__main__":
    main()
