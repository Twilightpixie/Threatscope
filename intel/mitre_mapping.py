MITRE_TECHNIQUES = {
    "reconnaissance_detected": {
        "id": "T1046",
        "name": "Network Service Scanning",
        "why": "This technique is often used to discover services before exploitation."
    },
    "brute_force_detected": {
        "id": "T1110",
        "name": "Brute Force",
        "why": "Repeated authentication attempts may indicate credential attacks."
    }
}

def print_mitre_mapping(reason):
    technique = MITRE_TECHNIQUES.get(reason)
    if not technique:
        return

    print("\nMapped Technique:")
    print(f"{technique['id']} – {technique['name']}")
    print("Why this matters:")
    print(technique["why"])
