#!/usr/bin/env python3
"""ThreatScope - Unified Main Orchestrator"""
import sys
from pathlib import Path
import structlog
from rich.console import Console
from config.settings import settings

console = Console()
logger = structlog.get_logger()

def initialize_system() -> bool:
    """Initialize all core components"""
    try:
        logger.info("🚀 Initializing ThreatScope", version="0.2.0")
        
        # TODO: Import and initialize modules
        # from ingestion.pipeline import LogIngestion
        # from ai_engine.detector import ThreatDetector
        # etc.
        
        console.print("[bold green]✅ ThreatScope System Initialized Successfully[/bold green]")
        return True
    except Exception as e:
        logger.error("❌ Initialization failed", error=str(e))
        console.print("[bold red]Initialization failed![/bold red]")
        return False

def main() -> None:
    if initialize_system():
        console.print("\n[bold cyan]Available modes:[/bold cyan]")
        console.print("   • python main_streaming.py     → Real-time Kafka mode")
        console.print("   • python -m threatscope         → Orchestrator mode")
        console.print("   • docker-compose up            → Full stack")
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
