"""
Unit tests — recon.time_window_features
Verifies that sliding-window feature extraction produces correct statistics.
"""

import pytest
from datetime import datetime, timezone, timedelta
from recon.time_window_features import extract_time_window_features


# ─── Helpers ──────────────────────────────────────────────────────────────────

def _ts(offset_seconds: int = 0) -> str:
    base = datetime(2025, 3, 12, 14, 30, 0, tzinfo=timezone.utc)
    return (base + timedelta(seconds=offset_seconds)).isoformat()


def make_event(src_ip="192.168.1.1", dst_ip="10.0.0.1",
               src_port=12345, dst_port=80,
               protocol="TCP", action="ALLOW",
               bytes_in=1000, offset=0):
    return {
        "timestamp": _ts(offset),
        "src_ip": src_ip,
        "dst_ip": dst_ip,
        "src_port": src_port,
        "dst_port": dst_port,
        "protocol": protocol,
        "action": action,
        "bytes_in": bytes_in,
    }


# ─── Tests ────────────────────────────────────────────────────────────────────

class TestExtractTimeWindowFeatures:
    def test_returns_list(self):
        events = [make_event(offset=i) for i in range(5)]
        result = extract_time_window_features(events, window_seconds=60)
        assert isinstance(result, list)

    def test_empty_input(self):
        result = extract_time_window_features([], window_seconds=60)
        assert result == []

    def test_single_window_returned(self):
        """All events within 60s → exactly one window."""
        events = [make_event(offset=i) for i in range(10)]  # 0-9s, all in one window
        result = extract_time_window_features(events, window_seconds=60)
        assert len(result) == 1

    def test_two_windows_returned(self):
        """Events spanning >60s → at least two windows."""
        events = (
            [make_event(offset=i) for i in range(5)] +          # window 1
            [make_event(offset=i + 65) for i in range(5)]        # window 2
        )
        result = extract_time_window_features(events, window_seconds=60)
        assert len(result) >= 2

    def test_feature_dict_keys(self):
        events = [make_event(offset=i) for i in range(5)]
        result = extract_time_window_features(events, window_seconds=60)
        expected_keys = {
            "connection_count", "unique_src_ips", "unique_dst_ips",
            "unique_dst_ports", "total_bytes",
        }
        for window in result:
            assert expected_keys.issubset(window.keys()), \
                f"Missing keys: {expected_keys - window.keys()}"

    def test_connection_count_correct(self):
        events = [make_event(offset=i) for i in range(7)]
        result = extract_time_window_features(events, window_seconds=60)
        assert result[0]["connection_count"] == 7

    def test_unique_src_ips_counted(self):
        events = [
            make_event(src_ip="10.0.0.1", offset=0),
            make_event(src_ip="10.0.0.2", offset=1),
            make_event(src_ip="10.0.0.1", offset=2),   # duplicate
        ]
        result = extract_time_window_features(events, window_seconds=60)
        assert result[0]["unique_src_ips"] == 2

    def test_unique_dst_ports_counted(self):
        events = [
            make_event(dst_port=80,  offset=0),
            make_event(dst_port=443, offset=1),
            make_event(dst_port=80,  offset=2),   # duplicate
            make_event(dst_port=22,  offset=3),
        ]
        result = extract_time_window_features(events, window_seconds=60)
        assert result[0]["unique_dst_ports"] == 3

    def test_port_scan_signature(self):
        """Many unique ports from one IP → feature should be high."""
        events = [make_event(dst_port=p, offset=i) for i, p in enumerate(range(200, 350))]
        result = extract_time_window_features(events, window_seconds=60)
        assert result[0]["unique_dst_ports"] == 150


class TestWindowSeconds:
    def test_window_seconds_respected(self):
        """A 30s window should split events that span 60s into 2 windows."""
        events = (
            [make_event(offset=i) for i in range(5)] +
            [make_event(offset=i + 35) for i in range(5)]
        )
        result = extract_time_window_features(events, window_seconds=30)
        assert len(result) >= 2
