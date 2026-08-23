from dataclasses import dataclass

from app.automation.automation_engine import Automation
from app.automation.automation_logger import log_execution


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


def execute_automation(automation: Automation) -> ExecutionResult:
    validation = validate_automation(automation)

    if not validation.success:
        log_execution(
            validation.automation_id,
            validation.success,
            validation.message,
        )
        return validation

    if automation.action == "TEST_ACTION":
        result = ExecutionResult(
            success=True,
            automation_id=automation.id,
            message="TEST_ACTION executed successfully.",
        )
        log_execution(
            result.automation_id,
            result.success,
            result.message,
        )
        return result

    result = ExecutionResult(
        success=False,
        automation_id=automation.id,
        message=f"Unsupported automation action: {automation.action}",
    )
    log_execution(
        result.automation_id,
        result.success,
        result.message,
    )
    return result
