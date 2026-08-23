from dataclasses import dataclass

from app.automation.automation_engine import Automation


@dataclass
class ExecutionResult:
    success: bool
    automation_id: str
    message: str


def validate_automation(automation: Automation) -> ExecutionResult:
    if not automation.id:
        return ExecutionResult(
            success=False,
            automation_id="",
            message="Automation ID is missing.",
        )

    if not automation.name:
        return ExecutionResult(
            success=False,
            automation_id=automation.id,
            message="Automation name is missing.",
        )

    if not automation.action:
        return ExecutionResult(
            success=False,
            automation_id=automation.id,
            message="Automation action is not configured.",
        )

    return ExecutionResult(
        success=True,
        automation_id=automation.id,
        message="Automation is ready for execution.",
    )
