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


async def automation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        format_automations(load_automations())
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
    application.add_handler(CommandHandler("status", status))
    application.add_handler(CommandHandler("dashboard", dashboard))
    application.add_handler(CommandHandler("log", log))
    application.add_handler(CommandHandler("tasks", tasks))
    application.add_handler(CommandHandler("automation", automation))
    application.add_handler(ConversationHandler(entry_points=[CommandHandler("create_task", start_task_creation)], states={1: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_task_id)], 2: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_task_title)], 3: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_task_description)]}, fallbacks=[]))
    application.add_handler(ConversationHandler(entry_points=[CommandHandler("update_status", start_status_update)], states={10: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_status_task_id)], 11: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_status_value)]}, fallbacks=[]))
    application.add_handler(CommandHandler("help", help_command))

    print("SLH Ground Station bot starting...")
    application.run_polling()


if __name__ == "__main__":
    main()
