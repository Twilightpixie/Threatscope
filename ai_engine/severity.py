def confidence_to_severity(confidence):
    if confidence >= 0.8:
        return "CRITICAL"
    elif confidence >= 0.5:
        return "HIGH"
    elif confidence >= 0.2:
        return "MEDIUM"
    else:
        return "LOW"
