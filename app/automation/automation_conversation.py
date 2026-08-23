from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from app.automation.automation_engine import AutomationStatus
from app.automation.automation_store import load_automations, set_automation_status


AUTOMATION_ID, AUTOMATION_STATUS = range(20, 22)


async def start_automation_status(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> int:
    await update.message.reply_text(
        "🔄 Update Automation Status\n\n"
        "Send the automation ID:"
    )
    return AUTOMATION_ID


async def receive_automation_id(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> int:
    automation_id = update.message.text.strip()

    automations = load_automations()

    if not any(automation.id == automation_id for automation in automations):
        await update.message.reply_text(
            "❌ Automation not found.\n"
            "Send a valid automation ID:"
        )
        return AUTOMATION_ID

    context.user_data["automation_id"] = automation_id

    await update.message.reply_text(
        "Choose the new status:\n\n"
        "READY\n"
        "DISABLED"
    )

    return AUTOMATION_STATUS


async def receive_automation_status(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> int:
    status_text = update.message.text.strip().upper()

    allowed_statuses = {
        "READY": AutomationStatus.READY,
        "DISABLED": AutomationStatus.DISABLED,
    }

    if status_text not in allowed_statuses:
        await update.message.reply_text(
            "❌ Invalid status.\n\n"
            "Choose:\n"
            "READY\n"
            "DISABLED"
        )
        return AUTOMATION_STATUS

    automation_id = context.user_data["automation_id"]
    status = allowed_statuses[status_text]

    updated = set_automation_status(
        automation_id,
        status,
    )

    context.user_data.pop("automation_id", None)

    if not updated:
        await update.message.reply_text(
            "❌ Automation update failed."
        )
        return ConversationHandler.END

    await update.message.reply_text(
        f"✅ Automation updated!\n"
        f"{automation_id} — Status: {status.value}"
    )

    return ConversationHandler.END
