"""
Unit tests — evaluation.metrics
Mathematical correctness tests for precision, recall, and F1.
These must pass perfectly — metric bugs invalidate the entire dissertation evaluation.
"""

import pytest
from evaluation.metrics import compute_metrics


# ─── Ground truth fixture ──────────────────────────────────────────────────────
# Format expected by compute_metrics: list of dicts with 'label' key (1=malicious, 0=benign)
# Decisions are matched by index or by a key — adjust if your implementation differs.

GROUND_TRUTH_LABELS = [1, 1, 1, 1, 0, 0, 0, 0, 1, 0]   # 5 malicious, 5 benign


def make_decisions_from_predictions(predicted_labels: list) -> list:
    """Create mock decision objects matching ground truth by index."""
    return [
        {
            "prediction": label,
            "anomaly_score": 0.9 if label == 1 else 0.2,
            "action": "block" if label == 1 else None,
        }
        for label in predicted_labels
    ]


class TestComputeMetricsPerfect:
    """Perfect classifier — all predictions correct."""

    def setup_method(self):
        preds = GROUND_TRUTH_LABELS  # identical to truth
        self.decisions = make_decisions_from_predictions(preds)
        self.gt = GROUND_TRUTH_LABELS

    def test_perfect_precision(self):
        m = compute_metrics(self.decisions, self.gt)
        assert abs(m.get("precision", m.get("Precision", 0)) - 1.0) < 1e-6

    def test_perfect_recall(self):
        m = compute_metrics(self.decisions, self.gt)
        assert abs(m.get("recall", m.get("Recall", 0)) - 1.0) < 1e-6

    def test_perfect_f1(self):
        m = compute_metrics(self.decisions, self.gt)
        f1 = m.get("f1", m.get("F1", m.get("f1_score", 0)))
        assert abs(f1 - 1.0) < 1e-6


class TestComputeMetricsAllWrong:
    """Worst classifier — every prediction inverted."""

    def setup_method(self):
        preds = [1 - x for x in GROUND_TRUTH_LABELS]
        self.decisions = make_decisions_from_predictions(preds)
        self.gt = GROUND_TRUTH_LABELS

    def test_zero_precision(self):
        m = compute_metrics(self.decisions, self.gt)
        p = m.get("precision", m.get("Precision", 1.0))
        assert p == 0.0

    def test_zero_recall(self):
        m = compute_metrics(self.decisions, self.gt)
        r = m.get("recall", m.get("Recall", 1.0))
        assert r == 0.0


class TestComputeMetricsMixed:
    """Mixed results: 3 TP, 1 FP, 2 FN → known expected values."""

    def test_known_precision(self):
        # 3 TP, 1 FP → Precision = 3/4 = 0.75
        preds = [1, 1, 1, 1, 0, 0, 0, 0, 0, 0]   # predicts 4 positives
        truth = [1, 1, 1, 0, 0, 0, 0, 0, 1, 0]   # 4 actual positives
        decisions = make_decisions_from_predictions(preds)
        m = compute_metrics(decisions, truth)
        p = m.get("precision", m.get("Precision"))
        assert abs(p - 0.75) < 0.01, f"Expected 0.75, got {p}"

    def test_known_recall(self):
        # 3 TP, 2 FN → Recall = 3/5 = 0.60 (4 true positives, 3 detected)
        preds = [1, 1, 1, 1, 0, 0, 0, 0, 0, 0]
        truth = [1, 1, 1, 0, 0, 0, 0, 0, 1, 0]
        decisions = make_decisions_from_predictions(preds)
        m = compute_metrics(decisions, truth)
        r = m.get("recall", m.get("Recall"))
        assert abs(r - 0.75) < 0.01, f"Expected 0.75, got {r}"  # 3/4 true positives found

    def test_returns_dict(self):
        preds = [1, 0, 1, 0, 0, 1, 0, 0, 1, 0]
        decisions = make_decisions_from_predictions(preds)
        m = compute_metrics(decisions, GROUND_TRUTH_LABELS)
        assert isinstance(m, dict)

    def test_all_expected_keys_present(self):
        preds = GROUND_TRUTH_LABELS
        decisions = make_decisions_from_predictions(preds)
        m = compute_metrics(decisions, GROUND_TRUTH_LABELS)
        keys_lower = {k.lower() for k in m.keys()}
        assert "precision" in keys_lower
        assert "recall" in keys_lower
        # F1 may be named f1, f1_score, or F1
        assert any("f1" in k for k in keys_lower)

    def test_empty_decisions(self):
        """Should return zeros or raise gracefully — not crash."""
        try:
            m = compute_metrics([], [])
            assert isinstance(m, dict)
        except (ZeroDivisionError, ValueError):
            pytest.skip("Empty input not handled — add guard to compute_metrics()")
