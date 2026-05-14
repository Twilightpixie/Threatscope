from collections import defaultdict
from datetime import datetime
from typing import Any, Dict, List

def extract_time_window_features(parsed_logs: List[Dict[str, Any]], window_seconds: int = 60) -> List[Dict[str, Any]]:
    by_ip: Dict[str, list] = defaultdict(list)
    for entry in parsed_logs:
        ts = entry["timestamp"]
        if isinstance(ts, str):
            ts = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        by_ip[entry["src_ip"]].append({**entry, "timestamp": ts})

    results = []
    for ip, events in by_ip.items():
        events.sort(key=lambda e: e["timestamp"])
        best = {"ports": set(), "count": 0, "dst_ips": set(), "pc": defaultdict(int), "dbp": defaultdict(set)}
        for i, start in enumerate(events):
            t0 = start["timestamp"]
            window = [e for e in events[i:] if (e["timestamp"] - t0).total_seconds() <= window_seconds]
            ports   = {e["dst_port"] for e in window}
            dst_ips = {e["dst_ip"]   for e in window}
            pc = defaultdict(int)
            dbp = defaultdict(set)
            for e in window:
                pc[e["dst_port"]] += 1
                dbp[e["dst_port"]].add(e["dst_ip"])
            if len(ports) * 3 + len(window) > len(best["ports"]) * 3 + best["count"]:
                best = {"ports": ports, "count": len(window), "dst_ips": dst_ips, "pc": pc, "dbp": dbp}
        results.append({
            "src_ip":           ip,
            "unique_ports":     len(best["ports"]),
            "connection_count": best["count"],
            "unique_dst_ips":   len(best["dst_ips"]),
            "port_counts":      dict(best["pc"]),
            "dst_ips_by_port":  {p: len(ips) for p, ips in best["dbp"].items()},
            "timestamps":       [e["timestamp"] for e in events],
            "time_window":      f"{window_seconds} seconds",
        })
    return results