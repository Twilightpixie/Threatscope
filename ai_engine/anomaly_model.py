from ai_engine.confidence import compute_confidence
from ai_engine.severity import confidence_to_severity

def detect_anomalies(features):
    decisions = []

    for feature in features:
        src_ip = feature["src_ip"]
        unique_ports = feature.get("unique_ports", 0)

        # Simple logic for now (research-friendly)
        anomaly = unique_ports >= 4
        confidence = min(unique_ports / 4, 1.0)

        severity = "LOW"
        if confidence >= 0.8:
            severity = "CRITICAL"
        elif confidence >= 0.4:
            severity = "MEDIUM"

        decisions.append({
            "src_ip": src_ip,
            "action": "block" if anomaly else "allow",
            "reason": "reconnaissance_detected" if anomaly else "normal_behavior",
            "confidence": round(confidence, 2),
            "severity": severity,
            "details": {
                "unique_ports": unique_ports,
                "time_window": "60 seconds"
            }
        })

    return decisions

