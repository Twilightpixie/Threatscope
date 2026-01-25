def explain_recon(decision):
    src_ip = decision.get("src_ip")
    confidence = decision.get("confidence", 0)
    ports = decision.get("unique_ports", "multiple")

    explanation = f"""
[WHY THIS ALERT?]

Source IP {src_ip} contacted {ports} different ports
within a short time window.

This behavior is commonly associated with
reconnaissance activity, where a threat actor
searches for open services before an attack.

Confidence Level: {confidence:.2f}
"""

    return explanation
