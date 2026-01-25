def rule_based_recon(features, port_threshold=5):
    results = []

    for f in features:
        if f["unique_ports"] >= port_threshold:
            results.append({
                "src_ip": f["src_ip"],
                "rule_alert": True
            })
        else:
            results.append({
                "src_ip": f["src_ip"],
                "rule_alert": False
            })

    return results
