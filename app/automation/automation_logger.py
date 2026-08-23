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
