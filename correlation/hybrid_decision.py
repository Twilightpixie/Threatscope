def hybrid_decision(rule_results, ai_results):
    ai_lookup = {a["src_ip"]: a["action"] for a in ai_results}

    final = []

    for r in rule_results:
        ip = r["src_ip"]

        if ai_lookup.get(ip) == "block" or r["rule_alert"]:
            final.append({
                "src_ip": ip,
                "action": "block",
                "reason": "hybrid_detection"
            })
        else:
            final.append({
                "src_ip": ip,
                "action": "allow",
                "reason": "normal"
            })

    return final

