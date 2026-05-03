#!/usr/bin/env python3
"""
ThreatScope — Unified Main Orchestrator  v0.3.0
================================================
Single entry point that wires every module together.
Previously this file had all imports commented out (TODO state).
This version is fully connected.

Execution modes:
    python threatscope.py               → batch mode (reads LOG_PATH)
    python threatscope.py --stream      → Kafka streaming mode
    python threatscope.py --eval-only   → run evaluation against ground truth
    python threatscope.py --help        → show this help

Configuration:
    All values come from config/settings.py.
    Override via environment variables or a .env file (see .env.example).
"""

import argparse
import sys

import structlog
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from config.settings import settings

# ── Pipeline modules ──────────────────────────────────────────────────────────
from ai_engine.anomaly_model import detect_anomalies
from correlation.mitre_enricher import enrich_with_mitre
from evaluation.ground_truth import GROUND_TRUTH
from evaluation.metrics import compute_metrics
from explain.explainer import explain_decision
from ids.ids_engine import apply_ids
from ingestion.elastic_writer import send_to_elastic
from ingestion.log_reader import read_logs
from ingestion.parser import parse_logs
from ips.ips_engine import apply_ips
from recon.narrative_timeline import build_narrative_timeline
from recon.narrative_view import print_narrative
from recon.time_window_features import extract_time_window_features
from recon.timeline import build_attack_timeline
from recon.timeline_view import print_timeline

console = Console()
logger = structlog.get_logger()


# ─────────────────────────────────────────────────────────────────────────────
# Initialisation
# ─────────────────────────────────────────────────────────────────────────────

def print_banner() -> None:
    console.print(Panel.fit(
        f"[bold cyan]ThreatScope SIEM[/bold cyan]  [dim]v{settings.VERSION}[/dim]\n"
        f"[dim]Log: {settings.LOG_PATH}  |  "
        f"ES: {settings.ES_HOST}:{settings.ES_PORT}  |  "
        f"IPS dry-run: {settings.IPS_DRY_RUN}[/dim]",
        border_style="cyan",
    ))


def initialize_system() -> bool:
    """Validate config and connectivity before running the pipeline."""
    try:
        logger.info("Initialising ThreatScope", version=settings.VERSION)

        # Warn if sensitive keys are missing (non-fatal)
        if not settings.VIRUSTOTAL_API_KEY:
            logger.warning("VIRUSTOTAL_API_KEY not set — threat intel enrichment disabled")
        if not settings.ABUSEIPDB_API_KEY:
            logger.warning("ABUSEIPDB_API_KEY not set — AbuseIPDB enrichment disabled")

        console.print("[bold green]✅ ThreatScope initialised[/bold green]")
        return True

    except Exception as exc:
        logger.error("Initialisation failed", error=str(exc))
        console.print(f"[bold red]❌ Initialisation failed: {exc}[/bold red]")
        return False


# ─────────────────────────────────────────────────────────────────────────────
# Batch pipeline
# ─────────────────────────────────────────────────────────────────────────────

def run_batch() -> None:
    """Full pipeline against a static log file."""
    console.rule("[cyan]Batch Mode[/cyan]")

    # 1. Ingest
    logger.info("Reading logs", path=settings.LOG_PATH)
    raw_logs = read_logs(settings.LOG_PATH)
    parsed_logs = parse_logs(raw_logs)
    logger.info("Logs parsed", count=len(parsed_logs))

    # 2. Feature extraction
    features = extract_time_window_features(
        parsed_logs, window_seconds=settings.WINDOW_SECONDS
    )

    # 3. AI detection + MITRE enrichment
    decisions = enrich_with_mitre(detect_anomalies(features))
    logger.info("Detections made", total=len(decisions))

    # 4. IDS / IPS / XAI
    apply_ids(decisions)
    for d in decisions:
        if d.get("action") == "block":
            explain_decision(d)
    apply_ips(decisions)

    # 5. Store to Elasticsearch
    for d in decisions:
        send_to_elastic(d)
    logger.info("Events stored to Elasticsearch")

    # 6. Evaluation
    _print_metrics(decisions)

    # 7. Timelines
    timelines = build_attack_timeline(parsed_logs, decisions)
    print_timeline(timelines)
    story = build_narrative_timeline(parsed_logs, decisions)
    print_narrative(story)

    console.print("\n[bold green]✅ ThreatScope batch run complete[/bold green]")


# ─────────────────────────────────────────────────────────────────────────────
# Streaming pipeline (Kafka)
# ─────────────────────────────────────────────────────────────────────────────

def run_streaming() -> None:
    """Consume from Kafka and process events in real time."""
    try:
        from kafka import KafkaConsumer  # type: ignore
        import json
    except ImportError:
        console.print("[red]kafka-python not installed. Run: pip install kafka-python[/red]")
        sys.exit(1)

    console.rule("[cyan]Streaming Mode[/cyan]")
    logger.info(
        "Starting Kafka consumer",
        servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        topic=settings.KAFKA_TOPIC,
    )

    consumer = KafkaConsumer(
        settings.KAFKA_TOPIC,
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        group_id=settings.KAFKA_GROUP_ID,
        auto_offset_reset=settings.KAFKA_AUTO_OFFSET_RESET,
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    )

    buffer: list = []
    console.print(f"[green]Listening on topic:[/green] {settings.KAFKA_TOPIC}")

    for message in consumer:
        buffer.append(message.value)

        # Process in windows of WINDOW_SECONDS worth of events
        if len(buffer) >= 100:          # simple count-based window for streaming
            features = extract_time_window_features(
                buffer, window_seconds=settings.WINDOW_SECONDS
            )
            decisions = enrich_with_mitre(detect_anomalies(features))
            apply_ids(decisions)
            for d in decisions:
                if d.get("action") == "block":
                    explain_decision(d)
            apply_ips(decisions)
            for d in decisions:
                send_to_elastic(d)
            buffer.clear()


# ─────────────────────────────────────────────────────────────────────────────
# Evaluation only
# ─────────────────────────────────────────────────────────────────────────────

def run_eval_only() -> None:
    """Re-run evaluation against existing decisions in ground truth."""
    console.rule("[cyan]Evaluation Mode[/cyan]")
    raw_logs = read_logs(settings.LOG_PATH)
    parsed_logs = parse_logs(raw_logs)
    features = extract_time_window_features(parsed_logs, window_seconds=settings.WINDOW_SECONDS)
    decisions = enrich_with_mitre(detect_anomalies(features))
    _print_metrics(decisions)


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def _print_metrics(decisions: list) -> None:
    metrics = compute_metrics(decisions, GROUND_TRUTH)
    table = Table(title="Evaluation Metrics", border_style="cyan")
    table.add_column("Metric", style="bold")
    table.add_column("Value", justify="right")
    for k, v in metrics.items():
        table.add_row(k, f"{v:.4f}" if isinstance(v, float) else str(v))
    console.print(table)


# ─────────────────────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="ThreatScope SIEM — AI-powered threat detection",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--stream", action="store_true", help="Kafka real-time streaming mode")
    group.add_argument("--eval-only", action="store_true", help="Run evaluation only")
    return parser.parse_args()


def main() -> None:
    print_banner()

    if not initialize_system():
        sys.exit(1)

    args = parse_args()

    if args.stream:
        run_streaming()
    elif args.eval_only:
        run_eval_only()
    else:
        run_batch()


if __name__ == "__main__":
    main()
