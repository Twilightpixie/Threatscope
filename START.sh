#!/bin/bash
cd ~/Threatscope
source venv/bin/activate
python main.py
cd ui
python3 -m http.server 8082 &
sleep 2
open http://localhost:8082
echo "ThreatScope is live at http://localhost:8082"
