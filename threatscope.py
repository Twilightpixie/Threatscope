#!/usr/bin/env python3
"""ThreatScope - Main Entry Point"""

import sys
import structlog
from rich.console import Console

console = Console()
logger = structlog.get_logger()


def main():
    logger.info("🚀 ThreatScope Starting", version="0.1.0", python=sys.version.split()[0])
    console.print("[bold green]ThreatScope v0.1.0[/bold green]")
    console.print("📌 Use [cyan]python main_streaming.py[/cyan] for full streaming mode")
    console.print("📌 Use [cyan]docker-compose up --build[/cyan] for complete stack")

    # TODO: Initialize core components here in future
    logger.info("✅ System initialized successfully")


if __name__ == "__main__":
    main()
