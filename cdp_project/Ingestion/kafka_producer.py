# ingestion/kafka_producer.py
from kafka import KafkaProducer
import json, time

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

sample_events = [
    {"loan_id": "L001", "customer_id": "CUST123", "status": "applied", "timestamp": "2026-06-21T21:59:00"},
    {"loan_id": "L002", "customer_id": "CUST456", "status": "approved", "timestamp": "2026-06-21T21:59:10"}
]

for event in sample_events:
    producer.send('loan.applications', event)
    print("Sent:", event)
    time.sleep(1)

producer.flush()
