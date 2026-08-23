import json
from datetime import datetime, timezone
from pathlib import Path


AUTOMATION_LOG_FILE = Path("automation_log.json")


def log_execution(
    automation_id: str,
    success: bool,
    message: str,
) -> None:
    if AUTOMATION_LOG_FILE.exists():
        data = json.loads(
            AUTOMATION_LOG_FILE.read_text(encoding="utf-8")
        )
    else:
        data = []

    data.append(
        {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "automation_id": automation_id,
            "success": success,
            "message": message,
        }
    )

    AUTOMATION_LOG_FILE.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def load_execution_log() -> list[dict]:
    if not AUTOMATION_LOG_FILE.exists():
        return []

    return json.loads(
        AUTOMATION_LOG_FILE.read_text(encoding="utf-8")
    )


def format_execution_log(limit: int = 10) -> str:
    entries = load_execution_log()

    if not entries:
        return "📜 No automation execution history."

    lines = ["📜 AUTOMATION EXECUTION HISTORY", ""]

    for entry in entries[-limit:]:
        status = "✅" if entry["success"] else "❌"
        lines.append(
            f"{status} {entry['automation_id']} — "
            f"{entry['message']}"
        )

    return "\n".join(lines)
