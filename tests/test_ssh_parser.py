from src.parsers.ssh_parser import parse_line

FAILED = "Oct 28 10:15:32 server sshd[1234]: Failed password for invalid user admin from 203.0.113.5 port 52144 ssh2"
OK = "Oct 28 10:16:01 server sshd[1240]: Accepted password for alice from 198.51.100.7 port 40022 ssh2"
NOISE = "Oct 28 10:16:05 server CRON[999]: session opened for user root"

def test_failed_login():
    e = parse_line(FAILED)
    assert e["user"] == "admin"
    assert e["ip"] == "203.0.113.5"
    assert e["success"] is False

def test_accepted_login():
    e = parse_line(OK)
    assert e["user"] == "alice"
    assert e["success"] is True

def test_irrelevant_line_ignored():
    assert parse_line(NOISE) is None