"""Central configuration for ThreatScope"""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).parent.parent


class Settings:
    # Kafka
    KAFKA_BOOTSTRAP_SERVERS: str = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    KAFKA_TOPIC: str = os.getenv("KAFKA_TOPIC", "threatscope-logs")

    # Elasticsearch
    ES_HOST: str = os.getenv("ES_HOST", "localhost")
    ES_PORT: int = int(os.getenv("ES_PORT", 9200))

    # AI Settings
    ANOMALY_THRESHOLD: float = 0.85
    MODEL_PATH: str = str(BASE_DIR / "ai_engine" / "models")

    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")


settings = Settings()
