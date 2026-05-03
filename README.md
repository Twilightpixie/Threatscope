# 🛡️ ThreatScope SIEM

**An AI-powered Security Information and Event Management system built for MSc Cybersecurity research.**

ThreatScope combines machine learning anomaly detection, MITRE ATT&CK enrichment, automated IDS/IPS response, and explainable AI (XAI) into a modular, production-realistic pipeline.

[![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)](https://python.org)
[![Elasticsearch](https://img.shields.io/badge/Elasticsearch-8.x-orange?logo=elasticsearch)](https://elastic.co)
[![Kafka](https://img.shields.io/badge/Apache_Kafka-7.x-black?logo=apachekafka)](https://kafka.apache.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green)](LICENSE)

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    DATA INGESTION LAYER                      │
│  logs/network.log → log_reader → parser → elastic_writer   │
│                    Kafka (main_streaming.py)                 │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              FEATURE EXTRACTION (60s sliding window)         │
│         recon/time_window_features.py                        │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│            AI ANOMALY DETECTION ENGINE                       │
│         ai_engine/anomaly_model.py  (Isolation Forest)      │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│            MITRE ATT&CK ENRICHMENT                          │
│         correlation/mitre_enricher.py                        │
└────────┬──────────────┬──────────────┬──────────────────────┘
         │              │              │
         ▼              ▼              ▼
    ┌─────────┐   ┌─────────┐   ┌───────────┐
    │   IDS   │   │   IPS   │   │ Explainer │
    │ engine  │   │ engine  │   │   (XAI)   │
    └────┬────┘   └────┬────┘   └─────┬─────┘
         └──────────────┴─────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│          THREAT INTEL + ELASTICSEARCH STORAGE                │
└────────────┬──────────────────────┬────────────────────────┘
             │                      │
             ▼                      ▼
    ┌──────────────┐      ┌────────────────────┐
    │  Evaluation  │      │  Attack Timeline   │
    │  (Precision, │      │  + Narrative View  │
    │  Recall, F1) │      │  (recon/)          │
    └──────────────┘      └────────────────────┘
                        │
                        ▼
              ┌──────────────────┐
              │   UI Dashboard   │
              │  (ui/index.html) │
              └──────────────────┘
```

---

## ⚡ Quick Start

### Option 1 — Docker (recommended, one command)

```bash
git clone https://github.com/Twilightpixie/Threatscope.git
cd Threatscope
cp .env.example .env          # configure your settings
docker-compose up -d          # starts ES, Kibana, Kafka, ThreatScope
```

Services available after startup:
- **ThreatScope UI** → `ui/index.html` (open in browser)
- **Kibana** → http://localhost:5601
- **Elasticsearch** → http://localhost:9200

### Option 2 — Local Python

```bash
git clone https://github.com/Twilightpixie/Threatscope.git
cd Threatscope

python -m venv .venv
source .venv/bin/activate     # Windows: .venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env          # edit with your ES/Kafka settings

python threatscope.py         # batch mode
python threatscope.py --stream   # Kafka streaming mode
python threatscope.py --eval-only  # evaluation only
```

---

## 📁 Project Structure

```
Threatscope/
├── ai_engine/          # ML anomaly detection (Isolation Forest)
├── correlation/        # MITRE ATT&CK enrichment
├── evaluation/         # Precision, Recall, F1 evaluation
├── explain/            # XAI — human-readable decision explanations
├── ids/                # Intrusion Detection System engine
├── ingestion/          # Log reader, parser, Elasticsearch writer
├── intel/              # Threat intelligence integration
├── ips/                # Intrusion Prevention System engine
├── logs/               # Log files (add your network.log here)
├── mitre/              # MITRE ATT&CK technique definitions
├── recon/              # Attack timeline + narrative reconstruction
├── simulation/         # Attack simulation for testing
├── tests/              # Unit test suite (pytest)
├── ui/                 # SOC dashboard (index.html)
├── config/             # Centralised configuration (settings.py)
├── threatscope.py      # Main orchestrator (entry point)
├── main.py             # Legacy batch runner
├── main_streaming.py   # Kafka streaming runner
├── docker-compose.yml  # Full stack deployment
├── Dockerfile          # ThreatScope container
├── requirements.txt    # Python dependencies
└── .env.example        # Configuration template
```

---

## ⚙️ Configuration

All configuration lives in `config/settings.py` and can be overridden via environment variables or a `.env` file. No hardcoded values.

Key settings:

| Variable | Default | Description |
|---|---|---|
| `LOG_PATH` | `logs/network.log` | Path to ingested log file |
| `WINDOW_SECONDS` | `60` | Feature extraction window size |
| `ANOMALY_BLOCK_THRESHOLD` | `0.75` | Score above which IPS auto-blocks |
| `ANOMALY_ALERT_THRESHOLD` | `0.50` | Score above which IDS raises alert |
| `ES_HOST` | `localhost` | Elasticsearch host |
| `ES_PORT` | `9200` | Elasticsearch port |
| `KAFKA_BOOTSTRAP_SERVERS` | `localhost:9092` | Kafka broker |
| `IPS_DRY_RUN` | `true` | If true, IPS logs blocks but doesn't apply them |

---

## 🔬 Running Tests

```bash
pip install -r requirements.txt
pytest                          # run all tests with coverage
pytest tests/test_parser.py     # single module
pytest -m "not integration"     # skip tests requiring live ES/Kafka
```

Test coverage targets:

| Module | Tests |
|---|---|
| `ingestion/parser.py` | `tests/test_parser.py` |
| `recon/time_window_features.py` | `tests/test_features.py` |
| `ai_engine/anomaly_model.py` | `tests/test_anomaly_model.py` |
| `ids/ids_engine.py` | `tests/test_ids_engine.py` |
| `ips/ips_engine.py` | `tests/test_ips_engine.py` |
| `correlation/mitre_enricher.py` | `tests/test_mitre_enricher.py` |
| `evaluation/metrics.py` | `tests/test_metrics.py` |

---

## 🧠 AI Engine

ThreatScope uses **Isolation Forest** for unsupervised anomaly detection over 60-second sliding windows. Features include:

- Connection count, rate, and failed connection ratio
- Unique source/destination IPs and destination ports
- Protocol distribution (TCP/UDP/ICMP ratio)
- Total bytes transferred (ingress + egress)

The model produces a continuous anomaly score in [0, 1]. Scores are then mapped to MITRE ATT&CK techniques by the enricher module.

---

## 🗺️ MITRE ATT&CK Coverage

Detected techniques are automatically mapped to the MITRE ATT&CK framework:

| Pattern | Technique | Tactic |
|---|---|---|
| Horizontal port scan (>50 unique ports) | T1046 | Discovery |
| SSH brute force (high failed conn ratio) | T1110 | Credential Access |
| Large outbound data transfer | T1041 | Exfiltration |
| Beaconing (periodic small connections) | T1071 | Command & Control |
| Internal east-west scanning | T1021 | Lateral Movement |

---

## 📊 Dashboard

Open `ui/index.html` directly in a browser. It will:
- Poll Elasticsearch every 4 seconds for live events
- Fall back to **demo mode** if Elasticsearch is unavailable (generates realistic simulated alerts)
- Show live anomaly score chart, severity distribution, MITRE ATT&CK heatmap, and alert feed

---

## 📚 Academic Context

ThreatScope was developed as an MSc Cybersecurity dissertation project. Key academic references:

- Liu et al. (2008) — *Isolation Forest* — IEEE ICDM
- Lundberg & Lee (2017) — *SHAP: A Unified Approach to Interpreting Model Predictions* — NIPS
- Strom et al. (2018) — *MITRE ATT&CK: Design and Philosophy*
- CICIDS2017 dataset — Canadian Institute for Cybersecurity

---

## 📄 Licence

MIT — see [LICENSE](LICENSE).
