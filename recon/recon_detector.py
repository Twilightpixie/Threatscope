def detect_recon(features, port_threshold=3):
    results = []

    for f in features:
        if f["unique_ports"] > port_threshold:
            verdict = "SUSPICIOUS (reconnaissance behavior)"
        else:
            verdict = "NORMAL"

        results.append({
            "src_ip": f["src_ip"],
            "unique_ports": f["unique_ports"],
            "verdict": verdict
        })

    return results
