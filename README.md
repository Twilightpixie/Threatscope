# ThreatScope — Explainable AI-Powered Modular SIEM

[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg)]()
[![Docker](https://img.shields.io/badge/Docker-ready-blue.svg)]()

**A modern, real-time Security Information and Event Management (SIEM) system with AI-driven threat detection, streaming correlation, MITRE ATT&CK mapping, and explainable alerts.**

## ✨ Key Features
- Real-time log ingestion (Kafka + Elasticsearch)
- Streaming event correlation engine
- Machine Learning anomaly detection + Rule-based IDS/IPS
- Automated MITRE ATT&CK technique & tactic mapping
- Explainable AI (SHAP / LIME) for every alert
- Attack simulation & automated evaluation framework
- Modular and extensible architecture

## 🏗️ Architecture
```mermaid
flowchart TD
    A[Log Sources] --> B[Ingestion Pipeline]
    B --> C[Streaming Layer (Kafka)]
    C --> D[Correlation Engine]
    D --> E[AI Engine + IDS/IPS]
    E --> F[Explainability Layer (SHAP/LIME)]
    F --> G[MITRE ATT&CK Mapper]
    G --> H[Alerting & Dashboard]
    I[Simulation & Threat Intel] --> C
# 1. Clone & Enter
git clone https://github.com/Twilightpixie/Threatscope.git
cd Threatscope

# 2. Create venv & Install
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Run
python threatscope.py          # Basic mode
# OR
python main_streaming.py       # Kafka streaming mode
Threatscope/
├── ai_engine/          # ML models
├── correlation/        # Event correlation
├── ingestion/          # Log collectors
├── ids/  ips/          # Intrusion modules
├── explain/            # XAI layer
├── mitre/              # ATT&CK integration
├── simulation/         # Attack simulation
├── evaluation/         # Benchmarking
├── ui/                 # Dashboard (FastAPI)
├── docs/
├── requirements.txt
├── threatscope.py
└── main_streaming.py

#### **2. Create docker-compose.yml (Recommended for Dissertation Demo)**
```bash
cat > docker-compose.yml << 'EOF'
version: '3.9'

services:
  zookeeper:
    image: confluentinc/cp-zookeeper:7.5.0
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_TICK_TIME: 2000

  kafka:
    image: confluentinc/cp-kafka:7.5.0
    depends_on:
      - zookeeper
    ports:
      - "9092:9092"
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1

  elasticsearch:
    image: elasticsearch:8.15.0
    ports:
      - "9200:9200"
    environment:
      discovery.type: single-node
      xpack.security.enabled: "false"

  threatscope:
    build: .
    depends_on:
      - kafka
      - elasticsearch
    environment:
      - KAFKA_BOOTSTRAP_SERVERS=kafka:9092
      - ES_HOST=elasticsearch
    ports:
      - "8000:8000"
    volumes:
      - .:/app
    command: uvicorn ui.main:app --host 0.0.0.0 --port 8000 --reload
