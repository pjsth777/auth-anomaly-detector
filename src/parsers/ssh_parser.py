import re
from datetime import datetime
from typing import Optional

SSH_LINE = re.compile(
    r"^(?P<ts>\w{3}\s+\d+\s[\d:]{8}) \S+ sshd\[\d+\]: "
    r"(?P<status>Failed|Accepted) (?P<method>password|publickey) "
    r"for (?:invalid user )?(?P<user>\S+) from (?P<ip>[\d.]+)"
)

def parse_line(line: str, year: int = 2026) -> Optional[dict]:
    m = SSH_LINE.match(line)
    if not m:
        return None
    ts = datetime.strptime(f"{year} {m['ts']}", "%Y %b %d %H:%M:%S")
    return {
        "time": ts,
        "user": m["user"],
        "ip": m["ip"],
        "method": m["method"],
        "success": m["status"] == "Accepted",
    }

def parse_file(path: str, year: int = 2026) -> list[dict]:
    events = []
    with open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            event = parse_line(line, year)
            if event:
                events.append(event)
    return events