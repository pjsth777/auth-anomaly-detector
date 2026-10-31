from src.parsers.windows_parser import parse_row

def test_failed_logon():
    row = {"TimeCreated": "2026-10-28T10:15:32", "Id": "4625",
           "User": "administrator", "IP": "203.0.113.5"}
    e = parse_row(row)
    assert e["success"] is False
    assert e["user"] == "administrator"
    assert e["ip"] == "203.0.113.5"

def test_successful_logon():
    row = {"TimeCreated": "2026-10-28T10:16:01", "Id": "4624",
           "User": "alice", "IP": "198.51.100.7"}
    assert parse_row(row)["success"] is True

def test_local_ip_normalised():
    row = {"TimeCreated": "2026-10-28T10:16:01", "Id": "4624",
           "User": "alice", "IP": "-"}
    assert parse_row(row)["ip"] == "local"

def test_other_event_ignored():
    row = {"TimeCreated": "2026-10-28T10:16:01", "Id": "4688",
           "User": "alice", "IP": "-"}
    assert parse_row(row) is None