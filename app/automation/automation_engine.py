from dataclasses import dataclass
from enum import Enum


class AutomationStatus(str, Enum):
    DISABLED = "DISABLED"
    READY = "READY"
    RUNNING = "RUNNING"
    FAILED = "FAILED"


@dataclass
class Automation:
    id: str
    name: str
    status: AutomationStatus = AutomationStatus.DISABLED
    description: str = ""


def create_automation(
    automation_id: str,
    name: str,
    description: str = "",
) -> Automation:
    return Automation(
        id=automation_id,
        name=name,
        description=description,
    )


def update_automation_status(
    automation: Automation,
    status: AutomationStatus,
) -> Automation:
    automation.status = status
    return automation


def format_automations(automations: list[Automation]) -> str:
    if not automations:
        return "🤖 No automations yet."

    lines = ["🤖 SLH AUTOMATIONS", ""]

    for automation in automations:
        lines.append(
            f"{automation.id} — {automation.name} "
            f"[{automation.status.value}]"
        )

    return "\n".join(lines)


def set_automation_status(
    automation: Automation,
    status: AutomationStatus,
) -> Automation:
    automation.status = status
    return automation
