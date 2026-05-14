import argparse
import json
from pathlib import Path


TASKS_FILE = Path("tasks.json")


def load_tasks():
    if not TASKS_FILE.exists():
        return []
    with open(TASKS_FILE) as f:
        return json.load(f)


def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=2)


def cmd_add(title):
    tasks = load_tasks()
    next_id = max([t["id"] for t in tasks], default=0) + 1
    tasks.append({"id": next_id, "title": title, "done": False})
    save_tasks(tasks)
    print(f"[+] Added task #{next_id}: {title}")


def cmd_list():
    tasks = load_tasks()
    if not tasks:
        print("No tasks. Add one with: python main.py add <title>")
        return
    for task in tasks:
        status = "x" if task["done"] else " "
        print(f"[{status}] #{task['id']}: {task['title']}")


def cmd_done(task_id):
    tasks = load_tasks()
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        print(f"Task #{task_id} not found")
        return
    task["done"] = True
    save_tasks(tasks)
    print(f"[+] Marked task #{task_id} as done")


def cmd_delete(task_id):
    tasks = load_tasks()
    original_count = len(tasks)
    tasks = [t for t in tasks if t["id"] != task_id]
    if len(tasks) == original_count:
        print(f"Task #{task_id} not found")
        return
    save_tasks(tasks)
    print(f"[-] Deleted task #{task_id}")


def main():
    parser = argparse.ArgumentParser(prog="todo", description="Simple command-line todo list")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_p = subparsers.add_parser("add", help="Add a new task")
    add_p.add_argument("title", help="Task description")

    subparsers.add_parser("list", help="List all tasks")

    done_p = subparsers.add_parser("done", help="Mark a task as complete")
    done_p.add_argument("id", type=int, help="Task ID")

    delete_p = subparsers.add_parser("delete", help="Delete a task")
    delete_p.add_argument("id", type=int, help="Task ID")

    args = parser.parse_args()

    if args.command == "add":
        cmd_add(args.title)
    elif args.command == "list":
        cmd_list()
    elif args.command == "done":
        cmd_done(args.id)
    elif args.command == "delete":
        cmd_delete(args.id)


if __name__ == "__main__":
    main()
