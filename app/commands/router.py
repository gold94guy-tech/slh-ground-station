from telegram import Update
from telegram.ext import ContextTypes


async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    await update.message.reply_text(
        "🚀 SLH Ground Station\n\n"
        "📊 System\n"
        "/start — Start system\n"
        "/status — System status\n"
        "/dashboard — Control center\n"
        "/myid — Show Telegram ID\n"
        "\n"
        "📋 Tasks\n"
        "/tasks — Show tasks\n"
        "/create_task — Create a task\n"
        "/update_status — Update task status\n"
        "\n"
        "⚙️ Automation\n"
        "/automation — Show automations\n"
        "/automation_status — Update automation status\n"
        "/automation_log — Show execution log\n"
        "/automation_auth — Show authorization status\n"
        "/automation_set_auth <id> <on|off> — Change authorization\n"
        "\n"
        "📝 Logs\n"
        "/log — Show system log\n"
        "\n"
        "/help — Show this help"
    )
