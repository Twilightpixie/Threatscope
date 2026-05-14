import ipaddress

# Internal ranges that are ATTACKERS in our simulation
MALICIOUS_PRIVATE = [
    "172.16.0.0/12",    # lateral movement source range
    "192.168.0.0/16",   # DNS exfil + deprecated protocol attackers
]
_mal_nets = [ipaddress.ip_network(r) for r in MALICIOUS_PRIVATE]

# Internal ranges that are BENIGN workstations
BENIGN_RANGES = [
    "10.0.0.0/8",       # our clean workstations
]
_benign_nets = [ipaddress.ip_network(r) for r in BENIGN_RANGES]

class _AutoDict(dict):
    def get(self, ip, default=False):
        try:
            addr = ipaddress.ip_address(ip)
            # Benign workstations
            for net in _benign_nets:
                if addr in net:
                    return False
            # Known malicious private ranges
            for net in _mal_nets:
                if addr in net:
                    return True
            # All public/external IPs = threat
            return not addr.is_private
        except ValueError:
            return False
    def __contains__(self, ip):
        return True

GROUND_TRUTH = _AutoDict()
