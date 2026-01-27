from kafka import KafkaConsumer
import json

def consume_logs():
    consumer = KafkaConsumer(
        "network-logs",
        bootstrap_servers="localhost:9092",
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        group_id="threatscope-group",
        value_deserializer=lambda v: json.loads(v.decode("utf-8"))
    )

    print("🟣 [Kafka Consumer] Listening for logs...")

    for msg in consumer:
        yield msg.value

