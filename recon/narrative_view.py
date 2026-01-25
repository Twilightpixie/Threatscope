def print_narrative(timelines):
    print("\n=== ATTACK STORY MODE ===")

    for ip, events in timelines.items():
        print(f"\n📍 Threat Actor: {ip}")
        for e in events:
            print(e)
