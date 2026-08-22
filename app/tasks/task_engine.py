from dataclasses import dataclass
from enum import Enum


class TaskStatus(str, Enum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"
    BLOCKED = "BLOCKED"


@dataclass
class Task:
    id: str
    title: str
    status: TaskStatus = TaskStatus.OPEN
    description: str = ""


def format_tasks(tasks: list[Task]) -> str:
    if not tasks:
        return "📋 No tasks yet."

    lines = ["📋 SLH TASKS", ""]

    for task in tasks:
        lines.append(
            f"{task.id} — {task.title} [{task.status.value}]"
        )

    return "\n".join(lines)


def create_task(
    task_id: str,
    title: str,
    description: str = "",
) -> Task:
    return Task(
        id=task_id,
        title=title,
        description=description,
    )


def update_task_status(task: Task, status: TaskStatus) -> Task:
    task.status = status
    return task
