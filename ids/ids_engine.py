from ui.severity_style import severity_icon

def apply_ids(decisions):
    for d in decisions:
        icon = severity_icon(d["severity"])

        if d["action"] == "block":
            print(
                f"{icon} [IDS] ALERT | Severity: {d['severity']} | "
                f"Confidence: {d['confidence']:.2f} | "
                f"Source: {d['src_ip']} | Reason: {d['reason']}"
            )
        else:
            print(
                f"{icon} [IDS] OK | Severity: {d['severity']} | "
                f"Source: {d['src_ip']}"
            )
