from telegram import Update
from telegram.ext import ContextTypes


async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    await update.message.reply_text(
        "🚀 SLH Ground Station\n\n"
        "/start — Start system\n"
        "/help — Show help\n"
        "/automation — Show automations\n"
        "/automation_log — Show execution log\n"
        "/automation_auth — Show authorization status\n"
        "/automation_set_auth <id> <on|off> — Change authorization"
    )
