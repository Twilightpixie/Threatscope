from ui.severity_style import severity_icon

def apply_ips(decisions):
    for d in decisions:
        if d["action"] == "block":
            icon = severity_icon(d["severity"])
            print(f"{icon} [IPS] Blocking suspected recon IP: {d['src_ip']}")

