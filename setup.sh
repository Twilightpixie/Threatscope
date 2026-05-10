#!/bin/bash
set -e
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
BLUE='\033[0;34m'; CYAN='\033[0;36m'; BOLD='\033[1m'; NC='\033[0m'
echo ""
echo -e "${BOLD}${BLUE}╔══════════════════════════════════════════╗${NC}"
echo -e "${BOLD}${BLUE}║        ThreatScope SIEM — Setup          ║${NC}"
echo -e "${BOLD}${BLUE}╚══════════════════════════════════════════╝${NC}"
echo ""
echo -e "${CYAN}[1/5] Checking Docker...${NC}"
if ! command -v docker &>/dev/null; then echo -e "${RED}✗ Install Docker Desktop from https://docker.com${NC}"; exit 1; fi
if ! docker info &>/dev/null; then echo -e "${RED}✗ Docker is not running. Start Docker Desktop first.${NC}"; exit 1; fi
echo -e "${GREEN}✓ Docker is running${NC}"
echo -e "${CYAN}[2/5] Starting Elasticsearch...${NC}"
docker rm -f es-threatscope 2>/dev/null || true
docker run -d --name es-threatscope -p 9201:9200 -e "discovery.type=single-node" -e "xpack.security.enabled=false" docker.elastic.co/elasticsearch/elasticsearch:8.13.0 > /dev/null
echo -e "${YELLOW}  Waiting for Elasticsearch (30s)...${NC}"
for i in {1..15}; do sleep 2; curl -s "http://localhost:9201" > /dev/null 2>&1 && { echo -e "${GREEN}✓ Elasticsearch is up${NC}"; break; } || echo -n "."; done
echo -e "${CYAN}[3/5] Setting up Python environment...${NC}"
python3 -m venv venv
source venv/bin/activate
pip install -q requests structlog rich elasticsearch scikit-learn numpy pandas
echo -e "${GREEN}✓ Dependencies installed${NC}"
echo -e "${CYAN}[4/5] Running ThreatScope pipeline...${NC}"
python main.py
echo -e "${GREEN}✓ Events sent to Elasticsearch${NC}"
echo -e "${CYAN}[5/5] Starting dashboard...${NC}"
python3 -c "
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.request
class P(BaseHTTPRequestHandler):
    def do_OPTIONS(self): self.send_response(200); self._h(); self.end_headers()
    def do_GET(self): self.px()
    def do_POST(self): self.px()
    def px(self):
        url='http://localhost:9201'+self.path
        body=self.rfile.read(int(self.headers.get('Content-Length',0))) if self.command=='POST' else None
        try:
            req=urllib.request.Request(url,data=body,method=self.command); req.add_header('Content-Type','application/json')
            resp=urllib.request.urlopen(req); data=resp.read()
            self.send_response(200); self._h(); self.end_headers(); self.wfile.write(data)
        except Exception as e: self.send_response(500); self._h(); self.end_headers(); self.wfile.write(str(e).encode())
    def _h(self):
        self.send_header('Access-Control-Allow-Origin','*'); self.send_header('Access-Control-Allow-Methods','GET,POST,OPTIONS')
        self.send_header('Access-Control-Allow-Headers','Content-Type'); self.send_header('Content-Type','application/json')
    def log_message(self,*a): pass
print('CORS proxy on 9202'); HTTPServer(('',9202),P).serve_forever()
" &
sleep 1
cd ui && python3 -m http.server 8080 &
cd ..
sleep 1
echo ""
echo -e "${BOLD}${GREEN}╔══════════════════════════════════════════╗${NC}"
echo -e "${BOLD}${GREEN}║  ThreatScope LIVE → http://localhost:8080║${NC}"
echo -e "${BOLD}${GREEN}║  To re-ingest: python main.py            ║${NC}"
echo -e "${BOLD}${GREEN}╚══════════════════════════════════════════╝${NC}"
command -v open &>/dev/null && open "http://localhost:8080" || xdg-open "http://localhost:8080" 2>/dev/null || true
echo -e "${YELLOW}Press Ctrl+C to stop.${NC}"
wait
