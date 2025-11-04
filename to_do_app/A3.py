import json
from datetime import datetime, timedelta


FILE_NAME = "tasks.json"


def load_tasks():
    try:
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_tasks(tasks):
    with open(FILE_NAME, "w") as file:
        json.dump(tasks, file, indent=4)

# === ADD TASK ===
def add_task(tasks):
    description = input("Enter task description: ").strip()
    due_date = input("Enter due date (YYYY-MM-DD) or leave blank: ").strip()
    if due_date == "":
        due_date = None
    task = {
        "description": description,
        "due_date": due_date,
        "status": "Pending"
    }
    tasks.append(task)
    save_tasks(tasks)
    print("✅ Task added successfully!")

# === VIEW ALL TASKS ===
def view_tasks(tasks, filter_type="all"):
    if not tasks:
        print("No tasks found.")
        return

    print("\n=== TASK LIST ===")
    for i, task in enumerate(tasks, start=1):
        due_date = task["due_date"] if task["due_date"] else "N/A"
        status = task["status"]
        show = False

        if filter_type == "all":
            show = True
        elif filter_type == "completed" and status == "Completed":
            show = True
        elif filter_type == "pending" and status == "Pending":
            show = True
        elif filter_type == "due_soon":
            if task["due_date"]:
                try:
                    date_obj = datetime.strptime(task["due_date"], "%Y-%m-%d")
                    if 0 <= (date_obj - datetime.now()).days <= 3:
                        show = True
                except:
                    pass

        if show:
            print(f"{i}. {task['description']} | Due: {due_date} | Status: {status}")

# === MARK TASK AS COMPLETE ===
def mark_task_complete(tasks):
    view_tasks(tasks, "pending")
    try:
        task_no = int(input("Enter task number to mark as complete: "))
        tasks[task_no - 1]["status"] = "Completed"
        save_tasks(tasks)
        print("✅ Task marked as completed!")
    except (ValueError, IndexError):
        print("❌ Invalid task number.")

# === EDIT TASK ===
def edit_task(tasks):
    view_tasks(tasks)
    try:
        task_no = int(input("Enter task number to edit: "))
        task = tasks[task_no - 1]
        new_desc = input(f"Enter new description (or press Enter to keep '{task['description']}'): ").strip()
        new_due = input(f"Enter new due date (YYYY-MM-DD) or press Enter to keep '{task['due_date']}': ").strip()

        if new_desc:
            task["description"] = new_desc
        if new_due:
            task["due_date"] = new_due
        save_tasks(tasks)
        print("✏️ Task updated successfully!")
    except (ValueError, IndexError):
        print("❌ Invalid task number.")

# === DELETE TASK ===
def delete_task(tasks):
    view_tasks(tasks)
    try:
        task_no = int(input("Enter task number to delete: "))
        deleted = tasks.pop(task_no - 1)
        save_tasks(tasks)
        print(f"🗑️ Deleted task: {deleted['description']}")
    except (ValueError, IndexError):
        print("❌ Invalid task number.")

# === MAIN MENU ===
def main():
    tasks = load_tasks()

    while True:
        print("\n==== Command-Line To-Do List Manager ====")
        print("1. Add a new task")
        print("2. View all tasks")
        print("3. View completed tasks")
        print("4. View pending tasks")
        print("5. View tasks due soon (within 3 days)")
        print("6. Mark task as completed")
        print("7. Edit a task")
        print("8. Delete a task")
        print("9. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_task(tasks)
        elif choice == "2":
            view_tasks(tasks, "all")
        elif choice == "3":
            view_tasks(tasks, "completed")
        elif choice == "4":
            view_tasks(tasks, "pending")
        elif choice == "5":
            view_tasks(tasks, "due_soon")
        elif choice == "6":
            mark_task_complete(tasks)
        elif choice == "7":
            edit_task(tasks)
        elif choice == "8":
            delete_task(tasks)
        elif choice == "9":
            print("👋 Exiting To-Do List Manager. Goodbye!")
            break
        else:
            print("❌ Invalid choice. Try again.")

# === RUN PROGRAM ===
if __name__ == "__main__":
    main()
