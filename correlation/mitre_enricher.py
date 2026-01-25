from mitre.mappings import MITRE_RECON_MAPPING

def enrich_with_mitre(decisions):
    enriched = []

    for d in decisions:
        reason = d.get("reason", "normal_behavior")
        mapping = MITRE_RECON_MAPPING.get(reason, {})

        enriched.append({
            **d,
            "mitre": mapping
        })

    return enriched

