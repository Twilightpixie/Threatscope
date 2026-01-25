from collections import defaultdict

def extract_recon_features(parsed_logs):
    ip_ports = defaultdict(set)

    for entry in parsed_logs:
        ip_ports[entry["src_ip"]].add(entry["dst_port"])

    features = []
    for ip, ports in ip_ports.items():
        features.append({
            "src_ip": ip,
            "unique_ports": len(ports)
        })

    return features
def classify_recon(features, port_threshold=3):
    results = []

    for f in features:
        if f["unique_ports"] >= port_threshold:
            status = "SUSPICIOUS (possible reconnaissance)"
        else:
            status = "NORMAL"

        results.append({
            "src_ip": f["src_ip"],
            "unique_ports": f["unique_ports"],
            "status": status
        })

    return results

