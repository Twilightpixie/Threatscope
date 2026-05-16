# ThreatScope

**ThreatScope is an explainable AI-driven SIEM for cyber threat intelligence.**

It turns raw security logs into understandable attack stories, MITRE ATT&CK mappings, risk scores, audit trails, executive reports, and AI-assisted response plans. The goal is simple: make a SIEM powerful enough for analysts, but clear enough for beginners, managers, and CEOs.

[![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)](https://python.org)
[![Elasticsearch](https://img.shields.io/badge/Elasticsearch-8.x-orange?logo=elasticsearch)](https://elastic.co)
[![Explainable AI](https://img.shields.io/badge/Explainable%20AI-SIEM%20Copilot-8b5cf6)](#ai-copilot)
[![Live Demo](https://img.shields.io/badge/Live%20Demo-GitHub%20Pages-brightgreen)](https://twilightpixie.github.io/Threatscope/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green)](LICENSE)

---

## Live Demo

Open the GitHub Pages demo:

**https://twilightpixie.github.io/Threatscope/**

The hosted demo is a self-contained AI Copilot dashboard with simulated incidents, so anyone can explore ThreatScope without installing Python, Docker, or Elasticsearch.

---

## What ThreatScope Does

ThreatScope connects the full security workflow:

- Ingests and parses security logs
- Detects anomalies with an AI engine
- Maps activity to MITRE ATT&CK techniques
- Correlates related events into attack campaigns
- Generates IDS alerts and IPS-style block decisions
- Creates explainable audit trails for every decision
- Produces CEO-friendly and analyst-friendly reports
- Provides an AI Copilot for summaries, next actions, and beginner explanations

---

## AI Copilot

The AI Copilot is designed around four audiences:

| Mode | Purpose |
|---|---|
| Executive | Business impact, current protection, decision needed |
| SOC Analyst | Evidence, MITRE mapping, source/destination, confidence |
| Incident Response | Containment steps, triage plan, escalation guidance |
| Beginner Mode | Plain-English explanations for people new to cybersecurity |

The current GitHub Pages demo uses local deterministic AI logic so it works offline. The interface is structured so a real LLM API can later receive the selected incident, evidence pack, MITRE technique, risk score, persona, and analyst question.

More detail: [docs/AI_COPILOT.md](docs/AI_COPILOT.md)

---

## Quick Start

Run the full local pipeline:

```bash
git clone https://github.com/Twilightpixie/Threatscope.git
cd Threatscope
./setup.sh
```

The setup script starts Elasticsearch, installs dependencies, processes sample logs, and opens the dashboard at:

```text
http://localhost:8080
```

To run the pipeline again:

```bash
source venv/bin/activate
python main.py
```

To open only the standalone AI Copilot demo locally:

```bash
python3 -m http.server 8765
```

Then visit:

```text
http://localhost:8765/docs/
```

---

## Architecture

```text
logs/network.log
      |
      v
Ingestion -> Parser -> Elasticsearch Writer
      |
      v
AI Engine -> rule-based and explainable anomaly scoring
      |
      v
MITRE ATT&CK Enrichment
      |
      +--> IDS Engine -> alerts
      +--> IPS Engine -> block decisions
      +--> Explainable AI -> human-readable reasoning
      |
      v
Dashboard + AI Copilot + Audit Reports
```

---

## Project Structure

```text
Threatscope/
├── ai_engine/          # ML anomaly detection
├── correlation/        # MITRE ATT&CK enrichment
├── docs/               # GitHub Pages demo and docs
├── evaluation/         # Precision, recall, F1 metrics
├── explain/            # Explainable AI narratives
├── ids/                # Intrusion detection logic
├── ips/                # Intrusion prevention decisions
├── ingestion/          # Log reader, parser, Elasticsearch writer
├── intel/              # Threat intelligence helpers
├── logs/               # Sample network logs
├── mitre/              # MITRE ATT&CK technique data
├── recon/              # Attack timeline reconstruction
├── simulation/         # Attack simulation data
├── tests/              # Unit tests
├── ui/                 # Local dashboard UI
├── main.py             # Main pipeline entry point
├── setup.sh            # One-command setup script
└── requirements.txt
```

---

## MITRE ATT&CK Coverage

| Pattern | Technique | Tactic |
|---|---|---|
| Port scan | T1046 | Discovery |
| SSH brute force | T1110 / T1110.001 | Credential Access |
| Large outbound transfer | T1041 | Exfiltration |
| DNS or HTTPS beaconing | T1071 | Command and Control |
| SMB lateral movement | T1021.002 | Lateral Movement |
| WMI remote execution | T1047 | Execution |
| LDAP enumeration | T1087 | Discovery |

---

## Why ThreatScope Is Different

Traditional SIEMs often show alerts that require expert interpretation. ThreatScope focuses on explainability:

- **For analysts:** evidence, confidence, MITRE technique, and process chain
- **For executives:** business impact, risk score, decision needed, and containment status
- **For beginners:** cyber concepts explained in plain language
- **For audits:** immutable-style decision records and downloadable reports

ThreatScope is not just a dashboard. It is a security explanation system.

---

## Roadmap

- Real LLM-backed AI Copilot API
- Sigma rule import
- YARA and Suricata integration
- More MITRE ATT&CK coverage
- Case management workflow
- Slack/email/webhook alerting
- Role-based views for analyst, executive, and auditor personas
- Evidence integrity hashes for audit reports

---

## License

MIT — see [LICENSE](LICENSE).
