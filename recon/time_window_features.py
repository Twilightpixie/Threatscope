from collections import defaultdict
from datetime import datetime, timedelta

def extract_time_window_features(parsed_logs, window_seconds=60):
    features = defaultdict(lambda: {"ports": set(), "timestamps": []})

    for entry in parsed_logs:
        ts = entry["timestamp"]

        # ✅ FIX: Convert string timestamps (Kafka) → datetime
        if isinstance(ts, str):
            ts = datetime.fromisoformat(ts)

        ip = entry["src_ip"]
        features[ip]["ports"].add(entry["dst_port"])
        features[ip]["timestamps"].append(ts)

    results = []

    for ip, data in features.items():
        unique_ports = len(data["ports"])
        results.append({
            "src_ip": ip,
            "unique_ports": unique_ports,
            "time_window": f"{window_seconds} seconds"
        })

    return results

