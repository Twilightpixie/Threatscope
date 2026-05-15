import json, requests
ELASTIC_URL = "http://localhost:9200/threatscope-events/_doc"
LOGS_URL    = "http://localhost:9200/threatscope-logs/_doc"
HEADERS     = {"Content-Type": "application/json"}

def send_to_elastic(event):
    try:
        r = requests.post(ELASTIC_URL, headers=HEADERS, data=json.dumps(event, default=str), timeout=2)
        return r.status_code
    except Exception:
        return 0

def send_raw_logs(parsed_logs):
    sent = 0
    for entry in parsed_logs:
        try:
            requests.post(LOGS_URL, headers=HEADERS, data=json.dumps(entry, default=str), timeout=2)
            sent += 1
        except Exception:
            pass
    return sent