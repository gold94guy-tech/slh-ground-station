import json
from pathlib import Path

from app.tasks.task_engine import Task, TaskStatus


TASKS_FILE = Path("tasks.json")


def save_tasks(tasks: list[Task]) -> None:
    data = [
        {
            "id": task.id,
            "title": task.title,
            "status": task.status.value,
            "description": task.description,
        }
        for task in tasks
    ]

    TASKS_FILE.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def load_tasks() -> list[Task]:
    if not TASKS_FILE.exists():
        return []

    data = json.loads(TASKS_FILE.read_text(encoding="utf-8"))

    return [
        Task(
            id=item["id"],
            title=item["title"],
            status=TaskStatus(item["status"]),
            description=item.get("description", ""),
        )
        for item in data
    ]


def add_task(task: Task) -> None:
    tasks = load_tasks()
    tasks.append(task)
    save_tasks(tasks)


def update_task_status(task_id: str, status: TaskStatus) -> bool:
    tasks = load_tasks()

    for task in tasks:
        if task.id == task_id:
            task.status = status
            save_tasks(tasks)
            return True

    return False
