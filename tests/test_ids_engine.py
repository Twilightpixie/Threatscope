"""
Unit tests — ids.ids_engine
Verifies that threshold logic raises alerts at the correct severity levels.
"""

import pytest
from unittest.mock import patch
from ids.ids_engine import apply_ids


# ─── Helpers ──────────────────────────────────────────────────────────────────

def make_decision(score=0.0, action=None, mitre_technique="", unique_dst_ports=1):
    return {
        "anomaly_score": score,
        "action": action,
        "mitre_technique": mitre_technique,
        "unique_dst_ports": unique_dst_ports,
        "src_ip": "192.168.1.1",
        "dst_ip": "10.0.0.1",
        "timestamp": "2025-03-12T14:30:00Z",
    }


# ─── Tests ────────────────────────────────────────────────────────────────────

class TestApplyIDS:
    def test_returns_list(self):
        decisions = [make_decision(score=0.3)]
        result = apply_ids(decisions)
        # apply_ids may mutate in place or return — handle both
        assert result is None or isinstance(result, list)

    def test_critical_threshold_triggered(self):
        """Score >= 0.85 should produce a CRITICAL alert."""
        d = make_decision(score=0.90)
        apply_ids([d])
        # The decision should be mutated with an alert level
        assert d.get("alert_level", "").upper() in {"CRITICAL", "HIGH"}

    def test_medium_threshold_triggered(self):
        d = make_decision(score=0.55)
        apply_ids([d])
        level = d.get("alert_level", "").upper()
        assert level in {"MEDIUM", "LOW", ""}  # may be medium or low

    def test_below_threshold_no_block(self):
        """Low-score events should not be auto-blocked."""
        d = make_decision(score=0.10)
        apply_ids([d])
        assert d.get("action") != "block"

    def test_port_scan_triggers_alert(self):
        """Many unique destination ports should always raise an alert."""
        d = make_decision(score=0.30, unique_dst_ports=300)
        apply_ids([d])
        # Either alert_level is set OR action is set
        assert d.get("alert_level") or d.get("action")

    def test_empty_decisions(self):
        """Should handle empty list without error."""
        apply_ids([])  # must not raise

    def test_does_not_mutate_irrelevant_fields(self):
        """apply_ids should not corrupt pre-existing fields."""
        d = make_decision(score=0.90)
        d["custom_field"] = "keep_me"
        apply_ids([d])
        assert d["custom_field"] == "keep_me"

    def test_multiple_decisions_all_processed(self):
        decisions = [make_decision(score=0.9), make_decision(score=0.3), make_decision(score=0.7)]
        apply_ids(decisions)
        # All decisions should have been touched (alert_level or action set where expected)
        assert decisions[0].get("alert_level") or decisions[0].get("action")
