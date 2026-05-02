"""Kafka Producer for ThreatScope"""

import json
from typing import Any

from kafka import KafkaProducer


def json_serializer(obj: Any) -> Any:
    """Custom JSON serializer"""
    if isinstance(obj, (set, frozenset)):
        return list(obj)
    raise TypeError(f"Type {type(obj)} not serializable")


# Initialize producer
producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v, default=json_serializer).encode("utf-8"),
)

print("✅ Kafka Producer initialized")
