import statistics
__all__ = ["ThreatDetector"]

def detect_anomalies(features):
    decisions = []
    for f in features:
        src_ip      = f["src_ip"]
        unique_ports = f.get("unique_ports", 0)
        conn_count   = f.get("connection_count", 0)
        port_counts  = f.get("port_counts", {})
        dst_by_port  = f.get("dst_ips_by_port", {})
        all_ts       = sorted(f.get("timestamps", []))

        reason     = "normal_behavior"
        action     = "allow"
        confidence = 0.1
        severity   = "LOW"

        # Rule 1: port scan
        if unique_ports >= 10:
            reason, action = "reconnaissance_detected", "block"
            confidence = min(unique_ports / 10, 1.0)
            severity   = "CRITICAL"

        # Rule 2: SSH brute force — 15+ fast attempts
        elif port_counts.get(22, 0) >= 15:
            ssh_ts = all_ts
            gaps = [(ssh_ts[i+1]-ssh_ts[i]).total_seconds() for i in range(len(ssh_ts)-1)]
            fast_gaps = [g for g in gaps if g < 10]
            if len(fast_gaps) >= 10:
                reason, action = "ssh_brute_force", "block"
                confidence = min(port_counts[22] / 20, 1.0)
                severity   = "HIGH"

        # Rule 3: lateral movement
        elif dst_by_port.get(445, 0) >= 4:
            reason, action = "lateral_movement", "block"
            confidence = min(dst_by_port[445] / 10, 1.0)
            severity   = "CRITICAL"

        # Rule 4: DNS exfiltration
        elif dst_by_port.get(53, 0) >= 5:
            reason, action = "dns_exfiltration", "block"
            confidence = min(dst_by_port[53] / 10, 1.0)
            severity   = "HIGH"

        # Rule 5: C2 beacon — uses FULL timeline (beacons span hours)
        elif len(all_ts) >= 10 and unique_ports == 1:
            gaps = [(all_ts[i+1]-all_ts[i]).total_seconds() for i in range(len(all_ts)-1)]
            regular = [g for g in gaps if g < 300]
            if len(regular) >= 8:
                mean_gap = statistics.mean(regular)
                std_gap  = statistics.stdev(regular) if len(regular) > 1 else 0
                if std_gap < 5 and 15 <= mean_gap <= 120:
                    reason, action = "c2_beacon", "block"
                    confidence = max(0.7, round(1.0 - std_gap / 30, 2))
                    severity   = "HIGH"

        # Rule 6: RDP + SMB chain
        elif port_counts.get(3389, 0) >= 2 and (port_counts.get(445,0) >= 1 or port_counts.get(135,0) >= 1):
            reason, action = "rdp_smb_chain", "block"
            confidence = 0.85
            severity   = "HIGH"

        # Rule 7: web fuzzing
        elif sum(port_counts.get(p,0) for p in [80,8080,8443,8000,4443,9000]) >= 20:
            reason, action = "web_fuzzing", "block"
            confidence = 0.75
            severity   = "MEDIUM"

        # Rule 8: deprecated protocol sweep
        elif sum(1 for p in [21,23,25,110,143,69,513,514] if p in port_counts) >= 3:
            reason, action = "deprecated_protocol_sweep", "block"
            confidence = 0.70
            severity   = "MEDIUM"

        # Rule 9: mild recon
        elif unique_ports >= 4:
            reason, action = "reconnaissance_detected", "block"
            confidence = round(unique_ports / 10, 2)
            severity   = "MEDIUM"

        decisions.append({
            "src_ip": src_ip, "action": action, "reason": reason,
            "confidence": round(confidence, 2), "severity": severity,
            "details": {"unique_ports": unique_ports, "connection_count": conn_count, "time_window": "60 seconds"},
        })
    return decisions

def compute_confidence(feature):
    return round(min(feature.get("unique_ports", 0) / 10.0, 1.0), 2)
