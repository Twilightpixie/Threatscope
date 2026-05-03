"""
ThreatScope — Centralised Configuration
All hardcoded values that were scattered across modules now live here.
Override any setting with an environment variable or a .env file.

Usage:
    from config.settings import settings
    path = settings.LOG_PATH
"""

from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ThreatScopeSettings(BaseSettings):
    """
    Pydantic-validated settings.  Every value can be overridden by:
      1. A matching environment variable  (e.g. export ES_HOST=my-server)
      2. A .env file in the project root
      3. config.yaml (loaded separately by load_yaml_config below)
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ── Project ───────────────────────────────────────────────────────────────
    APP_NAME: str = "ThreatScope"
    VERSION: str = "0.3.0"
    DEBUG: bool = False

    # ── Log Ingestion ──────────────────────────────────────────────────────────
    LOG_PATH: str = "logs/network.log"          # was hardcoded in main.py
    LOG_ENCODING: str = "utf-8"

    # ── Feature Extraction ────────────────────────────────────────────────────
    WINDOW_SECONDS: int = 60                     # was hardcoded in main.py

    # ── AI Engine ─────────────────────────────────────────────────────────────
    ANOMALY_CONTAMINATION: float = Field(default=0.05, ge=0.0, le=0.5)
    ANOMALY_BLOCK_THRESHOLD: float = Field(default=0.75, ge=0.0, le=1.0)
    ANOMALY_ALERT_THRESHOLD: float = Field(default=0.50, ge=0.0, le=1.0)
    MODEL_PATH: str = "models/anomaly_model.joblib"

    # ── Elasticsearch ─────────────────────────────────────────────────────────
    ES_HOST: str = "localhost"
    ES_PORT: int = 9200
    ES_SCHEME: str = "http"
    ES_INDEX: str = "threatscope-events"
    ES_USER: str = ""
    ES_PASSWORD: str = ""

    @property
    def ES_URL(self) -> str:
        return f"{self.ES_SCHEME}://{self.ES_HOST}:{self.ES_PORT}"

    # ── Kafka ─────────────────────────────────────────────────────────────────
    KAFKA_BOOTSTRAP_SERVERS: str = "localhost:9092"
    KAFKA_TOPIC: str = "threatscope-logs"
    KAFKA_GROUP_ID: str = "threatscope-consumer"
    KAFKA_AUTO_OFFSET_RESET: str = "latest"

    # ── MITRE ATT&CK ──────────────────────────────────────────────────────────
    MITRE_DATA_PATH: str = "mitre/attack_data.json"

    # ── Threat Intelligence ───────────────────────────────────────────────────
    VIRUSTOTAL_API_KEY: str = ""
    ABUSEIPDB_API_KEY: str = ""
    INTEL_CACHE_TTL_SECONDS: int = 3600         # cache IOC lookups for 1 hour

    # ── IPS ───────────────────────────────────────────────────────────────────
    IPS_ENABLED: bool = True
    IPS_DRY_RUN: bool = True                    # True = log only, False = real blocks

    # ── Evaluation ────────────────────────────────────────────────────────────
    GROUND_TRUTH_PATH: str = "evaluation/ground_truth.json"


# ── Singleton ─────────────────────────────────────────────────────────────────
settings = ThreatScopeSettings()
