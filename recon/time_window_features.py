"""Time window feature extractor"""
from collections import defaultdict
from datetime import datetime
from typing import List, Dict, Any

def extract_time_window_features(
    parsed_logs: List[Dict[str, Any]], 
    window_seconds: int = 60
) -> List[Dict[str, Any]]:
    """Extract features from logs in a time window"""
    features: Dict[str, Dict[str, Any]] = defaultdict(lambda: {"ports": set(), "timestamps": []})

    for entry in parsed_logs:
        ts = entry["timestamp"]
        if isinstance(ts, str):
            ts = datetime.fromisoformat(ts.replace("Z", "+00:00"))

        ip = entry["src_ip"]
        features[ip]["ports"].add(entry["dst_port"])
        features[ip]["timestamps"].append(ts)

    results = []
    for ip, data in features.items():
        results.append({
            "src_ip": ip,
            "unique_ports": len(data["ports"]),
            "time_window": f"{window_seconds} seconds"
        })

    return results
