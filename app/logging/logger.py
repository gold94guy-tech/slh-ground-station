import json
from datetime import datetime, timezone
from pathlib import Path


LOG_FILE = Path("logs/events.jsonl")


def log_event(event_type: str, message: str) -> None:
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    event = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "type": event_type,
        "message": message,
    }

    with LOG_FILE.open("a", encoding="utf-8") as file:
        file.write(json.dumps(event, ensure_ascii=False) + "\n")


def read_events() -> list[dict]:
    if not LOG_FILE.exists():
        return []

    events = []

    with LOG_FILE.open("r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if line:
                events.append(json.loads(line))

    return events
