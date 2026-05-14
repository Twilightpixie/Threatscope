import random, os
from datetime import datetime, timedelta

BASE = datetime(2026, 5, 15, 9, 0, 0)
OUT  = os.path.join("logs", "network.log")

rows = []
def add(ts, src, dst, dpt): rows.append((ts, f"{ts.strftime('%Y-%m-%d %H:%M:%S')} {src} {dst} {dpt}"))
def bump(ts, s): return ts + timedelta(seconds=s)

t = BASE

# 40 SSH brute-forcers
ssh_attackers = [f"45.33.{random.randint(1,254)}.{random.randint(1,254)}" for _ in range(40)]
for src in ssh_attackers:
    for _ in range(random.randint(15, 50)):
        add(t, src, "10.0.0.1", 22); t = bump(t, random.uniform(0.3, 2))
    t = bump(t, 3)

# 20 port scanners
t = bump(BASE, 500)
ports = [21,22,23,25,53,80,110,143,443,445,3306,3389,5432,6379,8080,8443,9200,27017,3000,5000]
scanners = [f"198.51.{random.randint(1,254)}.{random.randint(1,254)}" for _ in range(20)]
for src in scanners:
    for p in random.sample(ports, random.randint(10, 20)):
        add(t, src, "10.0.0.1", p); t = bump(t, random.uniform(0.05, 0.3))
    t = bump(t, 5)

# 15 lateral movement IPs
t = bump(BASE, 1000)
for src in [f"172.16.{random.randint(0,5)}.{random.randint(1,50)}" for _ in range(15)]:
    for i in range(1, random.randint(6, 20)):
        add(t, src, f"10.0.0.{i}", 445); t = bump(t, random.uniform(1, 3))
    t = bump(t, 5)

# 10 C2 beacons
t = bump(BASE, 1500)
for src in [f"91.{random.randint(100,200)}.{random.randint(1,254)}.{random.randint(1,254)}" for _ in range(10)]:
    for _ in range(40):
        add(t, src, "10.0.0.1", 443); t = bump(t, 30 + random.uniform(-2, 2))
    t = bump(t, 10)

# 8 DNS exfiltrators
t = bump(BASE, 2000)
resolvers = ["8.8.8.8","8.8.4.4","1.1.1.1","1.0.0.1","9.9.9.9","149.112.112.112","208.67.222.222","77.88.8.8"]
for src in [f"192.168.{random.randint(1,5)}.{random.randint(100,200)}" for _ in range(8)]:
    for r in resolvers * 8:
        add(t, src, r, 53); t = bump(t, random.uniform(0.2, 0.8))
    t = bump(t, 5)

# 10 web fuzzers
t = bump(BASE, 2500)
for src in [f"203.0.{random.randint(100,200)}.{random.randint(1,254)}" for _ in range(10)]:
    for _ in range(60):
        add(t, src, "10.0.0.1", random.choice([80,8080,8443,8000,4443,9000]))
        t = bump(t, random.uniform(0.05, 0.4))
    t = bump(t, 5)

# 5 RDP+SMB attackers
t = bump(BASE, 3000)
for src in [f"203.0.113.{random.randint(1,50)}" for _ in range(5)]:
    for _ in range(15):
        add(t, src, "10.0.0.1", 3389); t = bump(t, random.uniform(1, 4))
    for p in [445, 135, 139]:
        for _ in range(5):
            add(t, src, "10.0.0.1", p); t = bump(t, 1.5)
    t = bump(t, 5)

# 200 benign hosts
t = bump(BASE, 60)
for i in range(20, 220):
    src = f"10.0.{i//100}.{i%100+1}"
    dst_port = random.choice([80, 443, 53, 22, 3306, 123])
    dst = random.choice(["10.0.0.1", "8.8.8.8", "10.0.0.2"])
    for _ in range(random.randint(3, 15)):
        add(t, src, dst, dst_port); t = bump(t, rando
for _ in range(random.randint(3, 15)):
        add(t, src, dst, dst_port); t = bump(t, random.uniform(5, 30))

rows.sort(key=lambda x: x[0])
os.makedirs("logs", exist_ok=True)
with open(OUT, "w") as f:
    for _, line in rows: f.write(line + "\n")

unique_ips = len(set(r[1].split()[1] for r in rows))
print(f"Wrote {len(rows)} events, {unique_ips} unique IPs -> {OUT}")
