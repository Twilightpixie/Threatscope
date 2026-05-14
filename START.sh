#!/bin/bash
cd ~/Threatscope
source venv/bin/activate

# Kill anything on these ports
pkill -f "http.server" 2>/dev/null
sleep 1

# Start Elasticsearch if not running
docker start es-threatscope 2>/dev/null || true
sleep 3

# Run pipeline
python main.py

# Start dashboard on a free port
for port in 8080 8081 8082 8083 8084 8085; do
    python3 -m http.server $port --directory ui &
    sleep 1
    if kill -0 $! 2>/dev/null; then
        echo "Dashboard at http://localhost:$port"
        open "http://localhost:$port"
        break
    fi
done

wait
