"""
ThreatScope — Rich Synthetic Log Generator
Drop into Threatscope/ and run:  python generate_logs.py
Writes logs/sample_logs.txt with 500+ events, 9 attack scenarios.
Also prints the GROUND_TRUTH dict for evaluation/ground_truth.py.
"""
import random, os
from datetime import datetime, timedelta

BASE = datetime(2026, 5, 10, 9, 0, 0)
OUT  = os.path.join("logs", "sample_logs.txt")

def fmt(ts, src, dst, dpt):
    return (
        f"{ts.strftime('%b %d %H:%M:%S')} firewall kernel: "
        f"[UFW BLOCK] IN=eth0 OUT= SRC={src} DST={dst} "
        f"PROTO=TCP DPT={dpt} SPT={random.randint(1024,65535)}"
    )

rows = []
def add(ts, src, dst, dpt): rows.append((ts, fmt(ts, src, dst, dpt)))
def bump(ts, s): return ts + timedelta(seconds=s)

# 1. SSH brute-force (3 IPs x 30 attempts each)
t = BASE
for src in ["192.168.1.100", "45.33.32.156", "185.220.101.5"]:
    for _ in range(30):
        add(t, src, "10.0.0.1", 22); t = bump(t, random.uniform(0.5, 2.5))
    t = bump(t, 5)

# 2. RDP + SMB chain
t = bump(BASE, 120)
for _ in range(8):
    add(t, "203.0.113.42", "10.0.0.1", 3389); t = bump(t, random.uniform(2, 6))
for p in [445, 135, 139, 137]:
    for _ in range(4):
        add(t, "203.0.113.42", "10.0.0.1", p); t = bump(t, 1.5)

# 3. Port scan (2 scanners, 20 ports each)
t = bump(BASE, 180)
ports = [21,22,23,25,53,80,110,143,443,445,3306,3389,5432,6379,8080,8443,9200,27017,3000,5000]
for scanner in ["198.51.100.5", "203.0.115.99"]:
    for p in ports:
        add(t, scanner, "10.0.0.1", p); t = bump(t, random.uniform(0.05, 0.3))
    t = bump(t, 10)

# 4. Lateral movement — SMB across /24
t = bump(BASE, 300)
for i in range(1, 25):
    for _ in range(2):
        add(t, "172.16.0.50", f"10.0.0.{i}", 445); t = bump(t, random.uniform(1, 3))

# 5. C2 beacon — 40 periodic HTTPS hits (~30 s intervals)
t = bump(BASE, 360)
for _ in range(40):
    add(t, "91.108.4.10", "10.0.0.1", 443); t = bump(t, 30 + random.uniform(-2, 2))

# 6. DNS exfiltration — 10 resolvers x 6 bursts = 60 queries
t = bump(BASE, 420)
resolvers = ["8.8.8.8","8.8.4.4","1.1.1.1","1.0.0.1","9.9.9.9",
             "149.112.112.112","208.67.222.222","77.88.8.8","94.140.14.14","185.228.168.9"]
for r in resolvers * 6:
    add(t, "192.168.1.105", r, 53); t = bump(t, random.uniform(0.3, 1.2))

# 7. Deprecated-protocol sweep
t = bump(BASE, 600)
for p in [21, 23, 25, 110, 143, 69, 513, 514]:
    for _ in range(3):
        add(t, "192.168.1.200", "10.0.0.1", p); t = bump(t, 5)

# 8. Web fuzzing burst
t = bump(BASE, 700)
for _ in range(50):
    add(t, "203.0.114.77", "10.0.0.1", random.choice([80,8080,8443,8000,4443,9000]))
    t = bump(t, random.uniform(0.1, 0.8))

# 9. Benign baseline
t = bump(BASE, 60)
legit = [("10.0.0.10","8.8.8.8",53),("10.0.0.11","10.0.0.1",443),
         ("10.0.0.12","10.0.0.1",80),("10.0.0.13","10.0.0.2",22),
         ("10.0.0.14","10.0.0.1",3306),("10.0.0.15","pool.ntp.org",123)]
for _ in range(80):
    src, dst, dpt = random.choice(legit)
    add(t, src, dst, dpt); t = bump(t, random.uniform(2, 15))

rows.sort(key=lambda x: x[0])
os.makedirs("logs", exist_ok=True)
with open(OUT, "w") as f:
    for _, line in rows: f.write(line + "\n")
print(f"Wrote {len(rows)} events  ->  {OUT}\n")

gt = {
    "192.168.1.100":True,"45.33.32.156":True,"185.220.101.5":True,
    "203.0.113.42":True,"198.51.100.5":True,"203.0.115.99":True,
    "172.16.0.50":True,"91.108.4.10":True,"192.168.1.105":True,
    "192.168.1.200":True,"203.0.114.77":True,
    "10.0.0.10":False,"10.0.0.11":False,"10.0.0.12":False,
    "10.0.0.13":False,"10.0.0.14":False,"10.0.0.15":False,
}
print("=" * 56)
print("Paste into  evaluation/ground_truth.py")
print("=" * 56)
print("GROUND_TRUTH = {")
for ip, v in gt.items(): print(f'    "{ip}": {v},')
print("}")
print()
print("Missing IDS rules to add in  ids/detector.py:")
print("  ssh_brute_force   same port 22, >=10 attempts / 60 s")
print("  lateral_movement  port 445, >=4 distinct dst IPs / 60 s")
print("  c2_beacon         same dst:port, stddev(intervals) < 5 s")
print("  dns_exfiltration  port 53, >=5 distinct dst IPs / 60 s")
print("  rdp_smb_chain     3389 then 445/135 from same src / 60 s")
print("  web_fuzzing       HTTP ports, >=20 requests / 30 s")
