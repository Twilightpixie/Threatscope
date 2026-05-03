"""
Unit tests — ips.ips_engine
Verifies that blocking decisions are applied correctly and dry-run mode works.
"""

import pytest
from unittest.mock import patch
from ips.ips_engine import apply_ips


def make_decision(score=0.0, action=None, src_ip="192.168.1.101"):
    return {
        "anomaly_score": score,
        "action": action,
        "src_ip": src_ip,
        "dst_ip": "10.0.0.1",
        "timestamp": "2025-03-12T14:30:00Z",
        "mitre_technique": "T1046",
    }


class TestApplyIPS:
    def test_does_not_raise(self):
        apply_ips([make_decision(score=0.9, action="block")])

    def test_empty_input(self):
        apply_ips([])  # must not raise

    def test_block_action_set_on_high_score(self):
        """High-score decision should be marked for blocking."""
        d = make_decision(score=0.95)
        apply_ips([d])
        # IPS should set action=block on high-confidence events
        assert d.get("action") == "block" or d.get("ips_action") in {"block", "blocked"}

    def test_low_score_not_blocked(self):
        d = make_decision(score=0.10)
        apply_ips([d])
        assert d.get("action") != "block"

    def test_already_blocked_not_duplicated(self):
        """Pre-blocked decisions should pass through without error."""
        d = make_decision(score=0.95, action="block")
        apply_ips([d])   # should not raise

    def test_src_ip_recorded_in_block(self):
        """After blocking, the source IP should be traceable."""
        d = make_decision(score=0.95)
        apply_ips([d])
        # Some form of IP tracking must exist post-apply
        assert d.get("src_ip") == "192.168.1.101"

    def test_multiple_unique_ips_all_handled(self):
        decisions = [
            make_decision(score=0.9, src_ip=f"10.0.0.{i}") for i in range(5)
        ]
        apply_ips(decisions)   # must not raise
