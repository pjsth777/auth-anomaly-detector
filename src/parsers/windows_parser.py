import csv
from datetime import datetime
from typing import Optional

FAILED_ID = "4625"
SUCCESS_ID = "4624"

def parse_row(row: dict) -> Optional[dict]:
    event_id = str(row.get("Id", "")).strip()
    if event_id not in (FAILED_ID, SUCCESS_ID):
        return None
    ip = (row.get("IP") or "").strip()
    if ip in ("", "-", "::1", "127.0.0.1"):
        ip = "local"
    try:
        ts = datetime.fromisoformat(row["TimeCreated"].strip())
    except (KeyError, ValueError):
        return None
    return {
        "time": ts,
        "user": (row.get("User") or "").strip(),
        "ip": ip,
        "method": "windows",
        "success": event_id == SUCCESS_ID,
    }

def parse_file(path: str) -> list[dict]:
    events = []
    with open(path, newline="", encoding="utf-8-sig", errors="replace") as f:
        for row in csv.DictReader(f):
            event = parse_row(row)
            if event:
                events.append(event)
    return events