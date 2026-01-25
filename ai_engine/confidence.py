def compute_confidence(feature):
    """
    Confidence is based on how aggressive the reconnaissance is.
    More unique ports = higher confidence.
    """

    ports = feature.get("unique_ports", 0)

    # Simple normalized confidence score
    if ports >= 10:
        confidence = 1.0
    else:
        confidence = ports / 10.0

    return round(confidence, 2)
