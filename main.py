#!/usr/bin/env python3
import json, os
from datetime import datetime

from ai_engine.anomaly_model import detect_anomalies
from correlation.mitre_enricher import enrich_with_mitre
from evaluation.ground_truth import GROUND_TRUTH
from evaluation.metrics import compute_metrics
from explain.explainer import explain_decision
from ids.ids_engine import apply_ids
from ingestion.elastic_writer import send_to_elastic, send_raw_logs
from ingestion.log_reader import read_logs
from ingestion.parser import parse_logs
from intel.threat_intel import enrich_with_intel
from ips.ips_engine import apply_ips
from recon.narrative_timeline import build_narrative_timeline
from recon.narrative_view import print_narrative
from recon.time_window_features import extract_time_window_features
from recon.timeline import build_attack_timeline
from recon.timeline_view import print_timeline

print("\n=== ThreatScope Starting ===")
raw_logs    = read_logs("logs/network.log")
parsed_logs = parse_logs(raw_logs)
print(f"Parsed {len(parsed_logs)} events from {len(set(e['src_ip'] for e in parsed_logs))} unique IPs")

features  = extract_time_window_features(parsed_logs, window_seconds=60)
decisions = enrich_with_intel(enrich_with_mitre(detect_anomalies(features)))

apply_ids(decisions)
for d in decisions:
    if d.get("action") == "block":
        explain_decision(d)
apply_ips(decisions)

for d in decisions:
    send_to_elastic(d)
raw_sent = send_raw_logs(parsed_logs)
print(f"Sent to Elasticsearch — decisions: {len(decisions)}, raw logs: {raw_sent}")

metrics   = compute_metrics(decisions, GROUND_TRUTH)
print("\n=== Evaluation Metrics ===")
for k, v in metrics.items():
    print(f"{k}: {v:.2f}" if isinstance(v, float) else f"{k}: {v}")

tp        = metrics["TP"]
fp        = metrics["FP"]
fn        = metrics["FN"]
precision = metrics["precision"]
recall    = metrics["recall"]
f1        = round(2*precision*recall/(precision+recall), 2) if (precision+recall) > 0 else 0.0
fpr       = round(fp / (fp + metrics["TN"]) * 100, 1) if (fp + metrics["TN"]) > 0 else 0.0

blocked_ips = {d["src_ip"] for d in decisions if d["action"] == "block"}
by_ip = {}
for e in parsed_logs:
    if e["src_ip"] in blocked_ips:
        by_ip.setdefault(e["src_ip"], []).append(e["timestamp"])
spans = []
for ip, times in by_ip.items():
    times.sort()
    spans.append((times[-1] - times[0]).total_seconds())
mttd_min = round((sum(spans)/len(spans))/60, 1) if spans else 0.0

os.makedirs("ui", exist_ok=True)
with open("ui/metrics.json", "w") as mf:
    json.dump({
        "f1": f1, "precision": round(precision, 2),
        "recall": round(recall, 2), "fp_rate": fpr,
        "mttd_min": mttd_min, "tp": tp, "fp": fp, "fn": fn,
        "blocked": sum(1 for d in decisions if d["action"] == "block"),
        "timestamp": datetime.now().isoformat()
    }, mf)
print(f"Metrics written to ui/metrics.json — F1={f1}, FPR={fpr}%, MTTD={mttd_min}min")

timelines = build_attack_timeline(parsed_logs, decisions)
print_timeline(timelines)
story = build_narrative_timeline(parsed_logs, decisions)
print_narrative(story)
print("\n=== ThreatScope Run Complete ===")
