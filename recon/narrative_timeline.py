from collections import defaultdict

def build_narrative_timeline(parsed_logs, decisions):
    """
    Builds a human-readable attack story per source IP
    """

    timelines = defaultdict(list)

    # Index decisions by IP
    decision_lookup = {d["src_ip"]: d for d in decisions}

    for entry in parsed_logs:
        ip = entry["src_ip"]
        time = entry["timestamp"].strftime("%H:%M:%S")

        timelines[ip].append(
            f"🕒 {time} – Connection attempt to port {entry['dst_port']}"
        )

    # Add detection & response milestones
    for ip, decision in decision_lookup.items():
        if decision["reason"] == "reconnaissance_detected":
            timelines[ip].append(
                "🕒 Pattern escalation detected (multiple services probed)"
            )
            timelines[ip].append(
                f"🕒 Confidence threshold crossed ({decision['confidence']:.2f})"
            )

            if decision["action"] == "block":
                timelines[ip].append(
                    "🛑 IPS action taken: Source blocked"
                )

    return timelines
