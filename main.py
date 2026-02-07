

def process_logs(parsed_logs):
    # Feature extraction
    features = extract_time_window_features(parsed_logs, window_seconds=60)

    # AI detection + MITRE
    decisions = enrich_with_mitre(detect_anomalies(features))

    # IDS
    apply_ids(decisions)

    # Explanations
    for d in decisions:
        if d.get("action") == "block":
            explain_decision(d)

    # IPS
    apply_ips(decisions)

    # Store results
    for d in decisions:
        send_to_elastic(d)

    return decisions
# =========================
# Imports (ONLY imports)
# =========================
from ingestion.log_reader import read_logs
from ingestion.parser import parse_logs
from ingestion.elastic_writer import send_to_elastic

from recon.time_window_features import extract_time_window_features
from ai_engine.anomaly_model import detect_anomalies

from correlation.mitre_enricher import enrich_with_mitre
from ids.ids_engine import apply_ids
from ips.ips_engine import apply_ips

from explain.explainer import explain_decision
from recon.timeline import build_attack_timeline
from recon.timeline_view import print_timeline
from recon.narrative_timeline import build_narrative_timeline
from recon.narrative_view import print_narrative

from evaluation.ground_truth import GROUND_TRUTH
from evaluation.metrics import compute_metrics


# =========================
# ThreatScope Pipeline
# =========================

print("\n=== ThreatScope Starting ===")

# 1.Ingest logs
raw_logs = read_logs("logs/network.log")
parsed_logs = parse_logs(raw_logs)

print("\n=== DEBUG: Parsed Logs ===")
print(parsed_logs)

# 2. Run ThreatScope core
decisions = process_logs(parsed_logs)

print("\u2705 Events sent to Elasticsearch")

# 3.Feature extraction
features = extract_time_window_features(parsed_logs, window_seconds=60)

# 4.AI detection + MITRE enrichment
decisions = enrich_with_mitre(detect_anomalies(features))
# 5. Store detections in Elastic (ADDED, SAFE)
from ingestion.elastic_writer import send_to_elastic

for d in decisions:
    send_to_elastic(d)

# 6.IDS alerts + explanations
apply_ids(decisions)
for d in decisions:
    if d.get("action") == "block":
        explain_decision(d)

# 7.IPS enforcement
apply_ips(decisions)

# 8.Store results in Elasticsearch
for decision in decisions:
    send_to_elastic(decision)

print("\u2705 Events sent to Elasticsearch")

# 9.Evaluation
print("\n=== DEBUG: Decisions ===")
for d in decisions:
    print(d)

metrics = compute_metrics(decisions, GROUND_TRUTH)

print("\n=== Evaluation Metrics ===")
for k, v in metrics.items():
    print(f"{k}: {v:.2f}" if isinstance(v, float) else f"{k}: {v}")

# 10.Technical timeline
timelines = build_attack_timeline(parsed_logs, decisions)
print_timeline(timelines)

# 11.Narrative (story) timeline
story = build_narrative_timeline(parsed_logs, decisions)
print_narrative(story)
