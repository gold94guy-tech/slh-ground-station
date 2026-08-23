import json
from pathlib import Path

from app.automation.automation_engine import Automation, AutomationStatus


AUTOMATIONS_FILE = Path("automations.json")


def save_automations(automations: list[Automation]) -> None:
    data = [
        {
            "id": automation.id,
            "name": automation.name,
            "status": automation.status.value,
            "description": automation.description,
        }
        for automation in automations
    ]

    AUTOMATIONS_FILE.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def load_automations() -> list[Automation]:
    if not AUTOMATIONS_FILE.exists():
        return []

    data = json.loads(
        AUTOMATIONS_FILE.read_text(encoding="utf-8")
    )

    return [
        Automation(
            id=item["id"],
            name=item["name"],
            status=AutomationStatus(item["status"]),
            description=item.get("description", ""),
        )
        for item in data
    ]


def add_automation(automation: Automation) -> None:
    automations = load_automations()
    automations.append(automation)
    save_automations(automations)


def update_automation_status(
    automation_id: str,
    status: AutomationStatus,
) -> bool:
    automations = load_automations()

    for automation in automations:
        if automation.id == automation_id:
            automation.status = status
            save_automations(automations)
            return True

    return False
