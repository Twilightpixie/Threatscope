def explain_decision(decision):
    """
    Human-readable explanation for beginners and non-technical users
    """

    ip = decision.get("src_ip")
    reason = decision.get("reason", "unknown")
    confidence = decision.get("confidence", 0)
    details = decision.get("details", {})

    print("\n[WHY THIS ALERT?]")

    if reason == "reconnaissance_detected":
        ports = details.get("unique_ports", "multiple")
        window = details.get("time_window", "a short time")

        print(f"{ip} contacted {ports} different ports within {window}.")
        print("This behavior is commonly associated with reconnaissance activity.")

    elif reason == "brute_force_detected":
        attempts = details.get("attempts", "many")
        print(f"{ip} made {attempts} repeated access attempts.")
        print("Repeated attempts in a short time may indicate a brute-force attack.")

    else:
        print(f"The system observed unusual behavior from {ip}.")
        print("Further investigation may be required.")

    print(f"Confidence level: {confidence:.2f}")
