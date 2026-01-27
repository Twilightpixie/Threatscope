import argparse

def run_batch():
    print("🟢 Running ThreatScope in BATCH mode")
    import main  # uses your existing batch pipeline

def run_stream():
    print("🟣 Running ThreatScope in STREAMING mode")
    import main_streaming  # uses your Kafka pipeline

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ThreatScope SIEM")
    parser.add_argument(
        "--mode",
        choices=["batch", "stream"],
        required=True,
        help="Run mode: batch (file-based) or stream (Kafka)"
    )
    args = parser.parse_args()

    if args.mode == "batch":
        run_batch()
    elif args.mode == "stream":
        run_stream()
