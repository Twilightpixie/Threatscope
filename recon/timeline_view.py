def print_timeline(timelines):
    for ip, data in timelines.items():
        verdict = data["verdict"]
        events = data["events"]

        print("\n=== Timeline for", ip, "===")

        for e in events:
            print(f"{e['timestamp']} → Port {e['dst_port']}")

        if verdict:
            print(
                f"VERDICT → Action: {verdict['action']}, "
                f"Severity: {verdict['severity']}, "
                f"Confidence: {verdict['confidence']:.2f}"
            )
