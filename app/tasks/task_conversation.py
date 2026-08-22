from telegram import Update
from telegram.ext import ContextTypes


async def start_task_creation(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> int:
    await update.message.reply_text(
        "🆕 Create Task\n\n"
        "Send the task ID:"
    )
    return 1


async def receive_task_id(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> int:
    task_id = update.message.text.strip()

    if not task_id:
        await update.message.reply_text(
            "⚠️ Task ID cannot be empty. Send it again:"
        )
        return 1

    context.user_data["new_task_id"] = task_id

    await update.message.reply_text(
        "📝 Got it.\n\n"
        "Now send the task title:"
    )
    return 2


async def receive_task_title(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> int:
    title = update.message.text.strip()

    if not title:
        await update.message.reply_text(
            "⚠️ Task title cannot be empty. Send it again:"
        )
        return 2

    context.user_data["new_task_title"] = title

    await update.message.reply_text(
        "📄 Optional description?\n\n"
        "Send a description, or send - to skip:"
    )
    return 3


async def receive_task_description(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> int:
    description = update.message.text.strip()

    if description == "-":
        description = ""

    task_id = context.user_data.get("new_task_id")
    title = context.user_data.get("new_task_title")

    if not task_id or not title:
        await update.message.reply_text(
            "⚠️ Task data is missing. Please start again with /create_task."
        )
        context.user_data.clear()
        return -1

    from app.tasks.task_engine import create_task
    from app.tasks.task_store import add_task

    task = create_task(
        task_id=task_id,
        title=title,
        description=description,
    )

    add_task(task)

    context.user_data.clear()

    await update.message.reply_text(
        f"✅ Task created!\n\n"
        f"{task.id} — {task.title}\n"
        f"Status: {task.status.value}"
    )

    return -1


async def start_status_update(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> int:
    await update.message.reply_text(
        "🔄 Update Task Status\n\n"
        "Send the task ID:"
    )
    return 10


async def receive_status_task_id(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> int:
    task_id = update.message.text.strip()

    if not task_id:
        await update.message.reply_text(
            "⚠️ Task ID cannot be empty. Send it again:"
        )
        return 10

    context.user_data["status_task_id"] = task_id

    await update.message.reply_text(
        "Choose the new status:\n\n"
        "OPEN\n"
        "IN_PROGRESS\n"
        "DONE\n"
        "BLOCKED"
    )
    return 11


async def receive_status_value(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> int:
    status_value = update.message.text.strip().upper()

    if status_value not in {"OPEN", "IN_PROGRESS", "DONE", "BLOCKED"}:
        await update.message.reply_text(
            "⚠️ Invalid status.\n\n"
            "Use: OPEN, IN_PROGRESS, DONE, or BLOCKED"
        )
        return 11

    task_id = context.user_data.get("status_task_id")

    if not task_id:
        await update.message.reply_text(
            "⚠️ Task ID is missing. Please start again."
        )
        context.user_data.clear()
        return -1

    from app.tasks.task_engine import TaskStatus
    from app.tasks.task_store import update_task_status

    updated = update_task_status(
        task_id,
        TaskStatus(status_value),
    )

    context.user_data.clear()

    if not updated:
        await update.message.reply_text(
            f"⚠️ Task not found: {task_id}"
        )
        return -1

    await update.message.reply_text(
        f"✅ Task updated!\n\n"
        f"{task_id} — Status: {status_value}"
    )

    return -1
