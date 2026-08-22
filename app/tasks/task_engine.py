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
