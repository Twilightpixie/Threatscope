"""
Shared pytest fixtures for ThreatScope test suite.
"""

import pytest
from datetime import datetime, timezone, timedelta


def make_timestamp(offset_seconds: int = 0) -> str:
    base = datetime(2025, 3, 12, 14, 30, 0, tzinfo=timezone.utc)
    return (base + timedelta(seconds=offset_seconds)).isoformat()


@pytest.fixture
def sample_parsed_logs():
    """Ten realistic parsed log events for use across multiple test modules."""
    return [
        {
            "timestamp": make_timestamp(i * 5),
            "src_ip": "192.168.1.101" if i < 7 else "10.0.0.55",
            "dst_ip": f"10.0.0.{i + 1}",
            "src_port": 50000 + i,
            "dst_port": [80, 443, 22, 3389, 53, 8080, 25, 21, 3306, 5432][i],
            "protocol": "TCP" if i % 3 != 0 else "UDP",
            "action": "ALLOW" if i % 4 != 0 else "DENY",
            "bytes_in": (i + 1) * 512,
        }
        for i in range(10)
    ]


@pytest.fixture
def port_scan_logs():
    """Simulates a horizontal port scan — 300 unique ports in 60 seconds."""
    return [
        {
            "timestamp": make_timestamp(i),
            "src_ip": "192.168.1.200",
            "dst_ip": "10.0.0.5",
            "src_port": 60000,
            "dst_port": 1000 + i,
            "protocol": "TCP",
            "action": "DENY",
            "bytes_in": 60,
        }
        for i in range(300)
    ]


@pytest.fixture
def brute_force_logs():
    """Simulates SSH brute force — repeated failures on port 22."""
    return [
        {
            "timestamp": make_timestamp(i),
            "src_ip": "203.0.113.42",
            "dst_ip": "10.0.0.15",
            "src_port": 40000 + i,
            "dst_port": 22,
            "protocol": "TCP",
            "action": "DENY",
            "bytes_in": 80,
        }
        for i in range(200)
    ]


@pytest.fixture
def normal_traffic_logs():
    """Simulates normal web browsing traffic."""
    return [
        {
            "timestamp": make_timestamp(i * 30),
            "src_ip": f"192.168.1.{10 + i}",
            "dst_ip": "93.184.216.34",
            "src_port": 50000 + i,
            "dst_port": 443,
            "protocol": "TCP",
            "action": "ALLOW",
            "bytes_in": 2000 + i * 100,
        }
        for i in range(10)
    ]
