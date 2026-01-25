from collections import defaultdict
from datetime import timedelta

def extract_time_window_features(parsed_logs, window_seconds=60):
    parsed_logs.sort(key=lambda x: x["timestamp"])

    # Each (IP, window) maps to a SET of ports
    windows = defaultdict(set)

    for entry in parsed_logs:
        window_start = entry["timestamp"] - timedelta(
            seconds=entry["timestamp"].second % window_seconds
        )

        windows[(entry["src_ip"], window_start)].add(entry["dst_port"])

    features = []
    for (ip, window), ports in windows.items():
        features.append({
            "src_ip": ip,
            "window_start": window,
            "unique_ports": len(ports)
        })

    return features

