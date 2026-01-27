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

# 2.Feature extraction
features = extract_time_window_features(parsed_logs, window_seconds=60)

# 3.AI detection + MITRE enrichment
decisions = enrich_with_mitre(detect_anomalies(features))
# 4. Store detections in Elastic (ADDED, SAFE)
from ingestion.elastic_writer import send_to_elastic

for d in decisions:
    send_to_elastic(d)

# 5.IDS alerts + explanations
apply_ids(decisions)
for d in decisions:
    if d.get("action") == "block":
        explain_decision(d)

# 6.IPS enforcement
apply_ips(decisions)

# 7.Store results in Elasticsearch
for decision in decisions:
    send_to_elastic(decision)

print("✅ Events sent to Elasticsearch")

# 8.Evaluation
print("\n=== DEBUG: Decisions ===")
for d in decisions:
    print(d)

metrics = compute_metrics(decisions, GROUND_TRUTH)

print("\n=== Evaluation Metrics ===")
for k, v in metrics.items():
    print(f"{k}: {v:.2f}" if isinstance(v, float) else f"{k}: {v}")

# 9.Technical timeline
timelines = build_attack_timeline(parsed_logs, decisions)
print_timeline(timelines)

# 10.Narrative (story) timeline
story = build_narrative_timeline(parsed_logs, decisions)
print_narrative(story)

