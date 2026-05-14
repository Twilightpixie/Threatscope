import ipaddress

_BAD_RANGES = ["185.220.0.0/16","45.33.0.0/16","198.51.100.0/24","203.0.113.0/24","80.94.92.0/24","91.108.0.0/16"]
_networks = [ipaddress.ip_network(r, strict=False) for r in _BAD_RANGES]
_TOR = ["185.220.","185.129.","199.87.","162.247."]

def enrich_with_intel(decisions):
    enriched = []
    for d in decisions:
        d = dict(d)
        ip = d.get("src_ip","")
        flags = []
        try:
            addr = ipaddress.ip_address(ip)
            for net in _networks:
                if addr in net:
                    flags.append(f"known_bad_range:{net}")
                    d["confidence"] = min(round(d.get("confidence",0)+0.15,2),1.0)
        except ValueError:
            pass
        for prefix in _TOR:
            if ip.startswith(prefix):
                flags.append("tor_exit_node")
                d["confidence"] = min(round(d.get("confidence",0)+0.20,2),1.0)
                break
        if flags:
            d["intel_flags"] = flags
            if d.get("severity") == "LOW": d["severity"] = "MEDIUM"
            elif d.get("severity") == "MEDIUM": d["severity"] = "HIGH"
        enriched.append(d)
    return enriched