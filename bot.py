import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, ConversationHandler, MessageHandler, filters
from app.commands.router import help_command
from app.dashboard.dashboard import get_dashboard
from app.tasks.task_engine import format_tasks
from app.tasks.task_store import load_tasks
from app.automation.automation_engine import format_automations
from app.automation.automation_store import load_automations
from app.automation.automation_store import set_automation_authorization
from app.automation.automation_logger import format_execution_log
from app.automation.automation_executor import execute_automation
from app.automation.automation_conversation import start_automation_status, receive_automation_id, receive_automation_status
from app.tasks.task_conversation import start_task_creation, receive_task_id, receive_task_title, receive_task_description, start_status_update, receive_status_task_id, receive_status_value


load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN is not set in .env")


async def tasks(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(format_tasks(load_tasks()))


async def dashboard(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(get_dashboard())


async def log(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    from app.logging.logger import read_events

    events = read_events()

    if not events:
        await update.message.reply_text("📝 No log events yet.")
        return

    lines = ["📝 SLH LOG", ""]

    for event in events[-10:]:
        lines.append(
            f"{event['timestamp']} — "
            f"{event['type']} — "
            f"{event['message']}"
        )

    await update.message.reply_text("\n".join(lines))


def is_admin(update: Update) -> bool:
    admin_id = os.getenv("TELEGRAM_ADMIN_ID")
    user = update.effective_user

    return bool(
        admin_id
        and user
        and str(user.id) == admin_id
    )


async def myid(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        f"Telegram User ID: {update.effective_user.id}"
    )


async def automation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        format_automations(load_automations())
    )

async def automation_log(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        format_execution_log()
    )


async def automation_run(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) != 1:
        await update.message.reply_text(
            "Usage: /automation_run <automation_id>"
        )
        return

    automation_id = context.args[0]
    automations = load_automations()

    automation = next(
        (item for item in automations if item.id == automation_id),
        None,
    )

    if automation is None:
        await update.message.reply_text(
            f"❌ Automation not found: {automation_id}"
        )
        return

    result = execute_automation(automation)

    status = "✅" if result.success else "🛑"

    await update.message.reply_text(
        f"{status} {result.automation_id}\n"
        f"{result.message}"
    )

async def automation_auth(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    automations = load_automations()

    if not automations:
        await update.message.reply_text(
            "🔐 No automations configured."
        )
        return

    lines = ["🔐 AUTOMATION AUTHORIZATION", ""]

    for automation in automations:
        status = "✅ AUTHORIZED" if automation.authorized else "🛑 BLOCKED"
        lines.append(
            f"{status} — {automation.id} — {automation.name}"
        )

    await update.message.reply_text("\n".join(lines))

async def automation_set_auth(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not is_admin(update):
        await update.message.reply_text(
            "⛔ Admin authorization required."
        )
        return

    if len(context.args) != 2:
        await update.message.reply_text(
            "Usage: /automation_set_auth <automation_id> <on|off>"
        )
        return

    automation_id = context.args[0]
    value = context.args[1].lower()

    if value not in {"on", "off"}:
        await update.message.reply_text(
            "Authorization value must be: on or off."
        )
        return

    authorized = value == "on"

    success = set_automation_authorization(
        automation_id,
        authorized,
    )

    if not success:
        await update.message.reply_text(
            f"❌ Automation not found: {automation_id}"
        )
        return

    status = "AUTHORIZED" if authorized else "BLOCKED"

    await update.message.reply_text(
        f"🔐 {automation_id}: {status}"
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("SLH Ground Station online.")


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "🟢 SYSTEM STATUS\n\n"
        "System: ONLINE\n"
        "Telegram: CONNECTED\n"
        "Task Engine: ONLINE"
    )


def main() -> None:
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("myid", myid))
    application.add_handler(CommandHandler("status", status))
    application.add_handler(CommandHandler("dashboard", dashboard))
    application.add_handler(CommandHandler("log", log))
    application.add_handler(CommandHandler("tasks", tasks))
    application.add_handler(CommandHandler("automation", automation))
    application.add_handler(CommandHandler("automation_run", automation_run))
    application.add_handler(CommandHandler("automation_log", automation_log))
    application.add_handler(CommandHandler("automation_auth", automation_auth))
    application.add_handler(CommandHandler("automation_set_auth", automation_set_auth))
    application.add_handler(ConversationHandler(entry_points=[CommandHandler("automation_status", start_automation_status)], states={20: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_automation_id)], 21: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_automation_status)]}, fallbacks=[]))
    application.add_handler(ConversationHandler(entry_points=[CommandHandler("create_task", start_task_creation)], states={1: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_task_id)], 2: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_task_title)], 3: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_task_description)]}, fallbacks=[]))
    application.add_handler(ConversationHandler(entry_points=[CommandHandler("update_status", start_status_update)], states={10: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_status_task_id)], 11: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_status_value)]}, fallbacks=[]))
    application.add_handler(CommandHandler("help", help_command))

    print("SLH Ground Station bot starting...")
    application.run_polling()


if __name__ == "__main__":
    main()
