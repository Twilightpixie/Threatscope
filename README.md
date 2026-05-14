# 🛡️ ThreatScope SIEM

**An AI-powered Security Information and Event Management system built for MSc Cybersecurity research.**

ThreatScope combines machine learning anomaly detection, MITRE ATT&CK enrichment, automated IDS/IPS response, and explainable AI (XAI) into a modular, production-realistic pipeline.

[![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)](https://python.org)
[![Elasticsearch](https://img.shields.io/badge/Elasticsearch-8.x-orange?logo=elasticsearch)](https://elastic.co)
[![Live Demo](https://img.shields.io/badge/Live%20Demo-Visit%20Here-brightgreen)](https://twilightpixie.github.io/Threatscope/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green)](LICENSE)

---

## 🌐 Live Demo

👉 **[Visit the live demo dashboard here](https://twilightpixie.github.io/Threatscope/)**

The demo runs with simulated data so anyone can explore the interface without setup.
For real live data from your own machine, follow the Quick Start below.

---

## ⚡ Quick Start — Run on Your Machine

**Prerequisites:** Python 3.10+, Docker Desktop (running)

```bash
git clone https://github.com/Twilightpixie/Threatscope.git
cd Threatscope
./setup.sh
```

That's it. The script will:
- Start Elasticsearch in Docker
- Install Python dependencies
- Process the sample log file
- Open the live dashboard at **http://localhost:8080** automatically

To ingest new logs and see the dashboard update live:
```bash
source venv/bin/activate
python main.py
```

---

## 🏗️ Architecturelogs/network.log
│
▼
[Ingestion] → parser → elastic_writer
│
▼
[AI Engine] — rule-based anomaly detection
│
▼
[MITRE ATT&CK Enrichment] — technique mapping
│
├── [IDS Engine] — alert generation
├── [IPS Engine] — auto-block decisions
└── [XAI] — human-readable explanations
│
▼
[Elasticsearch] → [Dashboard — ui/index.html]

---

## 📁 Project Structure
Threatscope/
├── ai_engine/        # ML anomaly detection (Isolation Forest)
├── correlation/      # MITRE ATT&CK enrichment
├── evaluation/       # Precision, Recall, F1 metrics
├── explain/          # Explainable AI (XAI)
├── ids/              # Intrusion Detection System
├── ips/              # Intrusion Prevention System
├── ingestion/        # Log reader, parser, Elasticsearch writer
├── intel/            # Threat intelligence
├── logs/             # Sample network.log included
├── mitre/            # MITRE ATT&CK technique definitions
├── recon/            # Attack timeline reconstruction
├── simulation/       # Attack simulation for testing
├── ui/               # SOC Dashboard (index.html)
├── main.py           # Pipeline entry point
├── setup.sh          # One-command setup script
└── requirements.txt

---

## 🧠 AI Engine

Uses **Isolation Forest** for unsupervised anomaly detection over 60-second sliding windows. Features include connection count, unique ports, protocol distribution, and bytes transferred. Anomaly scores map directly to MITRE ATT&CK techniques.

---

## 🗺️ MITRE ATT&CK Coverage

| Pattern | Technique | Tactic |
|---|---|---|
| Port scan (>50 unique ports) | T1046 | Discovery |
| SSH brute force | T1110 | Credential Access |
| Large outbound transfer | T1041 | Exfiltration |
| Periodic beaconing | T1071 | Command & Control |
| Internal SMB scanning | T1021 | Lateral Movement |

---

## 📄 Licence

MIT — see [LICENSE](LICENSE).
