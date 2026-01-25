from datetime import datetime

def parse_logs(raw_logs):
    parsed = []

    for line in raw_logs:
        parts = line.strip().split()
        if len(parts) < 5:
            continue

        timestamp = datetime.strptime(
            parts[0] + " " + parts[1],
            "%Y-%m-%d %H:%M:%S"
        )

        parsed.append({
            "timestamp": timestamp,
            "src_ip": parts[2],
            "dst_ip": parts[3],
            "dst_port": int(parts[4])
        })

    return parsed

