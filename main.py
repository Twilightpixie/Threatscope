from intel.mitre_mapping import print_mitre_mapping
from explain.counterfactual import print_counterfactual
from explain.learn_mode import print_tip
from recon.narrative_timeline import build_narrative_timeline
from recon.narrative_view import print_narrative
from explain.explainer import explain_decision
from correlation.mitre_enricher import enrich_with_mitre
from evaluation.ground_truth import GROUND_TRUTH
from evaluation.metrics import compute_metrics

from ingestion.log_reader import read_logs
from ingestion.parser import parse_logs

from recon.time_window_features import extract_time_window_features
from ai_engine.anomaly_model import detect_anomalies

from ids.ids_engine import apply_ids
from ips.ips_engine import apply_ips

from recon.timeline import build_attack_timeline
from recon.timeline_view import print_timeline


# 1. Ingest logs
raw_logs = read_logs("logs/network.log")
parsed_logs = parse_logs(raw_logs)
print("\n=== DEBUG: Parsed Logs ===")
print(parsed_logs)

# 2. Feature extraction (time-window recon features)
features = extract_time_window_features(parsed_logs, window_seconds=60)

# 3. AI anomaly detection
decisions = enrich_with_mitre(detect_anomalies(features))

# 4. IDS alerts
apply_ids(decisions)
for d in decisions:
    if d["action"] == "block":
        explain_decision(d)

# 5. IPS enforcement
apply_ips(decisions)

# 6. Evaluation metrics
print("\n=== DEBUG: Decisions ===")
for d in decisions:
    print(d)
metrics = compute_metrics(decisions, GROUND_TRUTH)

print("\n=== Evaluation Metrics ===")
for k, v in metrics.items():
    if isinstance(v, float):
        print(f"{k}: {v:.2f}")
    else:
        print(f"{k}: {v}")

# 7. Attack timeline
timelines = build_attack_timeline(parsed_logs, decisions)
print_timeline(timelines)

decisions = enrich_with_mitre(detect_anomalies(features))
timelines = build_narrative_timeline(parsed_logs, decisions)
print_narrative(timelines)
