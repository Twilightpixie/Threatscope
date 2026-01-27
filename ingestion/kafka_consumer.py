from datetime import datetime

def parse_event(event):
    if "timestamp" in event:
        event["timestamp"] = datetime.fromisoformat(event["timestamp"])
    return event
import json
from kafka import KafkaConsumer
from datetime import datetime

consumer = KafkaConsumer(
    "network-logs",
    bootstrap_servers="localhost:9092",
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    auto_offset_reset="earliest",
    enable_auto_commit=True,
for msg in consumer:
    yield parse_event(json.loads(msg.value))
)

def parse_kafka_event(event):
    # Convert timestamp back to datetime
    if "timestamp" in event:
        event["timestamp"] = datetime.fromisoformat(event["timestamp"])
    return event

def consume_logs():
    print("[Kafka Consumer] Waiting for logs...")
    for message in consumer:
        yield parse_kafka_event(message.value)
