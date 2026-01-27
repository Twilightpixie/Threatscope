import requests
import json

ELASTIC_URL = "http://localhost:9200/threatscope-events/_doc"

def send_to_elastic(event):
    headers = {"Content-Type": "application/json"}
    response = requests.post(
        ELASTIC_URL,
        headers=headers,
        data=json.dumps(event)
    )
    return response.status_code
