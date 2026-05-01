#!/usr/bin/env python3
"""ThreatScope Main Entry Point"""
import sys
from rich.console import Console

console = Console()

def main():
    console.print("[bold green]🚀 ThreatScope Starting...[/bold green]")
    console.print("📌 Run `python main_streaming.py` for full streaming mode")
    console.print("📌 Run `docker-compose up` for complete stack")
    # TODO: Add your main logic here later

if __name__ == "__main__":
    main()
