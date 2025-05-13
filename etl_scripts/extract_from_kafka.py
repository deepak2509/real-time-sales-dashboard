from kafka import KafkaConsumer
import json

def extract_sales_data(batch_size=100):
    consumer = KafkaConsumer(
        "sales_topic",
        bootstrap_servers="kafka:9092",
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        value_deserializer=lambda m: json.loads(m.decode("utf-8"))
    )
    records = []
    for msg in consumer:
        records.append(msg.value)
        if len(records) >= batch_size:
            break
    return records
