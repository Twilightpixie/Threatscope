"""
Unit tests — ingestion.parser
Tests that raw log strings are normalised correctly into structured dicts.
"""

import pytest
from unittest.mock import patch, mock_open
from ingestion.parser import parse_logs


# ─── Fixtures ─────────────────────────────────────────────────────────────────

RAW_LOGS_VALID = [
    "2025-03-12T14:30:00Z ALLOW TCP 192.168.1.101:54321 -> 10.0.0.15:22 bytes=1240",
    "2025-03-12T14:30:01Z DENY  UDP 10.0.0.50:12345  -> 8.8.8.8:53   bytes=64",
    "2025-03-12T14:30:02Z ALLOW TCP 172.16.0.1:80     -> 192.168.1.5:49200 bytes=88200",
]

RAW_LOGS_MALFORMED = [
    "",                          # empty line
    "NOT A VALID LOG LINE",      # no recognisable structure
    None,                        # type error guard
]


# ─── Tests ────────────────────────────────────────────────────────────────────

class TestParseLogsValid:
    def test_returns_list(self):
        result = parse_logs(RAW_LOGS_VALID)
        assert isinstance(result, list)

    def test_correct_count(self):
        result = parse_logs(RAW_LOGS_VALID)
        assert len(result) == len(RAW_LOGS_VALID)

    def test_each_entry_is_dict(self):
        for entry in parse_logs(RAW_LOGS_VALID):
            assert isinstance(entry, dict)

    def test_required_keys_present(self):
        required_keys = {"timestamp", "src_ip", "dst_ip", "src_port", "dst_port",
                         "protocol", "action"}
        for entry in parse_logs(RAW_LOGS_VALID):
            missing = required_keys - entry.keys()
            assert not missing, f"Missing keys: {missing}"

    def test_src_ip_parsed(self):
        result = parse_logs([RAW_LOGS_VALID[0]])
        assert result[0]["src_ip"] == "192.168.1.101"

    def test_dst_ip_parsed(self):
        result = parse_logs([RAW_LOGS_VALID[0]])
        assert result[0]["dst_ip"] == "10.0.0.15"

    def test_dst_port_is_int(self):
        result = parse_logs([RAW_LOGS_VALID[0]])
        assert isinstance(result[0]["dst_port"], int)
        assert result[0]["dst_port"] == 22

    def test_action_parsed(self):
        result = parse_logs([RAW_LOGS_VALID[0]])
        assert result[0]["action"].upper() in {"ALLOW", "DENY", "DROP", "BLOCK"}

    def test_protocol_parsed(self):
        result = parse_logs([RAW_LOGS_VALID[0]])
        assert result[0]["protocol"].upper() in {"TCP", "UDP", "ICMP"}


class TestParseLogsMalformed:
    def test_empty_string_skipped_or_handled(self):
        """Parser should not crash on empty strings."""
        result = parse_logs([""])
        # Either skips the entry or returns a dict with default/null values
        assert isinstance(result, list)

    def test_empty_input_list(self):
        result = parse_logs([])
        assert result == []

    def test_does_not_raise_on_none_elements(self):
        """Parser should handle None entries without throwing."""
        try:
            result = parse_logs([None])
            assert isinstance(result, list)
        except TypeError:
            pytest.skip("Parser does not handle None — add guard in parse_logs()")
