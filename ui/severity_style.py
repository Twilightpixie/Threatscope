def severity_icon(severity):
    """
    Maps severity levels to visual icons for better readability
    """

    mapping = {"LOW": "🟢", "MEDIUM": "🟡", "HIGH": "🔴", "CRITICAL": "🔴"}

    return mapping.get(severity, "⚪")
