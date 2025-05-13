import os
import json
import time
from kafka import KafkaProducer

# Kafka Configuration
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "sales_topic")
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "192.168.1.123:9092")  # Use host.docker.internal:9093 if running outside Docker

# Initialize Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def send_streamed_data(file_path="data_simulation/streamed_sales.json", delay=1):
    """
    Reads records from a JSON lines file and sends them to Kafka topic.
    """
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return

    with open(file_path, "r") as f:
        for line in f:
            if line.strip():
                try:
                    record = json.loads(line)
                    producer.send(KAFKA_TOPIC, value=record)
                    print(f"✅ Sent: {record}")
                    time.sleep(delay)
                except json.JSONDecodeError:
                    print("⚠️ Skipping invalid JSON line.")

    producer.flush()
    print("🎉 All records sent successfully.")

if __name__ == "__main__":
    send_streamed_data()
