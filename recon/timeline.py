from collections import defaultdict

def build_attack_timeline(parsed_logs, decisions):
    timelines = defaultdict(list)

    decision_lookup = {d["src_ip"]: d for d in decisions}

    for entry in parsed_logs:
        ip = entry["src_ip"]
        timelines[ip].append({
            "timestamp": entry["timestamp"],
            "dst_port": entry["dst_port"]
        })

    # Sort events by time
    for ip in timelines:
        timelines[ip].sort(key=lambda x: x["timestamp"])

    # Attach verdicts
    final_timelines = {}

    for ip, events in timelines.items():
        verdict = decision_lookup.get(ip, {})
        final_timelines[ip] = {
            "verdict": verdict,
            "events": events
        }

    return final_timelines
