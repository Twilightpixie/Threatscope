from ingestion.kafka_consumer import consume_logs
from recon.time_window_features import extract_time_window_features
from ai_engine.anomaly_model import detect_anomalies
from correlation.mitre_enricher import enrich_with_mitre
from ids.ids_engine import apply_ids
from ips.ips_engine import apply_ips
from explain.explainer import explain_decision

print("🚀 ThreatScope Streaming Mode Started")

buffer = []

for event in consume_logs():
    buffer.append(event)

    if len(buffer) >= 20:   # simple micro-batch
        features = extract_time_window_features(buffer, window_seconds=60)
        decisions = enrich_with_mitre(detect_anomalies(features))

        apply_ids(decisions)
        apply_ips(decisions)

        for d in decisions:
            explain_decision(d)

        buffer.clear()
