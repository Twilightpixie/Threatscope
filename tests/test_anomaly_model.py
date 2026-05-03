"""
Unit tests — ai_engine.anomaly_model
Verifies that detect_anomalies returns correct structure and sensible scores.
"""

import pytest
from ai_engine.anomaly_model import detect_anomalies


def make_feature_window(connection_count=10, unique_src_ips=3, unique_dst_ips=2,
                         unique_dst_ports=5, total_bytes=50000,
                         failed_conn_ratio=0.02, window_start="2025-03-12T14:30:00Z"):
    return {
        "window_start": window_start,
        "connection_count": connection_count,
        "unique_src_ips": unique_src_ips,
        "unique_dst_ips": unique_dst_ips,
        "unique_dst_ports": unique_dst_ports,
        "total_bytes": total_bytes,
        "failed_conn_ratio": failed_conn_ratio,
    }


class TestDetectAnomalies:
    def test_returns_list(self):
        features = [make_feature_window()]
        result = detect_anomalies(features)
        assert isinstance(result, list)

    def test_each_result_is_dict(self):
        features = [make_feature_window()]
        for d in detect_anomalies(features):
            assert isinstance(d, dict)

    def test_anomaly_score_key_present(self):
        features = [make_feature_window()]
        result = detect_anomalies(features)
        for d in result:
            assert "anomaly_score" in d, f"Missing anomaly_score in {d}"

    def test_anomaly_score_in_range(self):
        features = [make_feature_window()]
        result = detect_anomalies(features)
        for d in result:
            score = d["anomaly_score"]
            assert 0.0 <= score <= 1.0, f"Score out of [0,1]: {score}"

    def test_empty_input(self):
        result = detect_anomalies([])
        assert result == []

    def test_port_scan_scores_higher_than_normal(self):
        """Extreme port scan feature vector should score higher than normal traffic."""
        normal = make_feature_window(unique_dst_ports=3, connection_count=5)
        scan   = make_feature_window(unique_dst_ports=500, connection_count=1000,
                                     failed_conn_ratio=0.95)
        results = detect_anomalies([normal, scan])
        normal_score = results[0]["anomaly_score"]
        scan_score   = results[1]["anomaly_score"]
        assert scan_score >= normal_score, \
            f"Port scan ({scan_score:.3f}) should score >= normal ({normal_score:.3f})"

    def test_output_count_matches_input(self):
        features = [make_feature_window(window_start=f"2025-03-12T14:3{i}:00Z")
                    for i in range(5)]
        result = detect_anomalies(features)
        assert len(result) == 5

    def test_original_window_keys_preserved(self):
        f = make_feature_window()
        f["custom"] = "keep"
        result = detect_anomalies([f])
        assert result[0].get("custom") == "keep"
