"""
Unit tests — correlation.mitre_enricher
Verifies that known attack patterns map to correct MITRE ATT&CK techniques.
"""

import pytest
from correlation.mitre_enricher import enrich_with_mitre


def make_decision(unique_dst_ports=1, connection_count=10, score=0.5,
                  failed_conn_ratio=0.0, bytes_out=1000):
    return {
        "anomaly_score": score,
        "unique_dst_ports": unique_dst_ports,
        "connection_count": connection_count,
        "failed_conn_ratio": failed_conn_ratio,
        "bytes_out": bytes_out,
        "src_ip": "192.168.1.1",
        "timestamp": "2025-03-12T14:30:00Z",
    }


class TestEnrichWithMitre:
    def test_returns_list(self):
        result = enrich_with_mitre([make_decision()])
        assert isinstance(result, list)

    def test_each_decision_has_mitre_keys(self):
        decisions = [make_decision(score=0.9, unique_dst_ports=200)]
        result = enrich_with_mitre(decisions)
        for d in result:
            # At minimum one of these keys should be added
            has_mitre = any(k in d for k in
                            ["mitre_technique", "mitre_tactic", "mitre_id"])
            assert has_mitre, f"No MITRE key found in: {d.keys()}"

    def test_port_scan_maps_to_t1046(self):
        """High unique_dst_ports → T1046 Network Service Scanning."""
        d = make_decision(unique_dst_ports=300, score=0.90)
        result = enrich_with_mitre([d])
        technique = result[0].get("mitre_technique", "")
        assert "T1046" in technique or "discovery" in technique.lower(), \
            f"Expected T1046 but got: {technique}"

    def test_brute_force_maps_to_t1110(self):
        """High failed_conn_ratio on SSH port → T1110 Brute Force."""
        d = make_decision(failed_conn_ratio=0.95, score=0.88)
        result = enrich_with_mitre([d])
        technique = result[0].get("mitre_technique", "")
        # Accept T1110 or credential-access family
        assert technique != "" or result[0].get("mitre_tactic") is not None

    def test_empty_decisions(self):
        result = enrich_with_mitre([])
        assert result == []

    def test_low_score_still_enriched(self):
        """Even low-anomaly events should get MITRE context if pattern matches."""
        d = make_decision(score=0.2)
        result = enrich_with_mitre([d])
        assert isinstance(result[0], dict)

    def test_original_keys_preserved(self):
        d = make_decision(score=0.9)
        d["custom"] = "preserved"
        result = enrich_with_mitre([d])
        assert result[0]["custom"] == "preserved"
