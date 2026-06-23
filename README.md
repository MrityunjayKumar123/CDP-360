# CDP-360
Customer 360


# Customer Data Platform (CDP) Demo

This repository demonstrates an **end‑to‑end CDP pipeline** with small sample data, compatible with macOS and VSCode.dev environments.  

---

##  Overview

The pipeline includes:
- **Kafka** → Event ingestion from CRM, ERP, web, mobile, IoT, and social sources  
- **Spark Structured Streaming + Delta Lake** → Data processing (Bronze → Silver → Gold tables)  
- **PostgreSQL** → Operational fields for transactional consistency  
- **Python Identity Resolution** → Single Customer View (SCV)  
- **Feature Engineering** → Model‑ready features  
- **Great Expectations** → Data governance and compliance  

---

##  Prerequisites

- macOS with Docker Desktop installed  
- Python 3.10+  
- VSCode.dev connected to your GitHub repo  
- Homebrew (optional for local installs)  

---

## Project Structure

## Project Structure

```text
cdp_project/
├── docker-compose.yml
├── requirements.txt
├── ingestion/kafka_producer.py
├── processing/spark_streaming_job.py
├── identity_resolution/dedupe_job.py
├── features/feature_engineering.py
├── governance/great_expectations_checks.py
└── README.md





## **Step 1 – Start Infrastructure


docker-compose up -d

docker ps

## ** Step 2 – Create Kafka Topic**

docker exec -it kafka kafka-topics \
  --bootstrap-server localhost:9092 \
  --create --topic loan.applications \
  --partitions 1 --replication-factor 1

## **Step 3 – Install Python Libraries**

pip install -r requirements.txt

## Step 4 – Run Kafka Producer

python ingestion/kafka_producer.py

##** Step 5 – Run Spark Streaming Job**

python processing/spark_streaming_job.py


## **Step 6 – Feature Engineering**

python features/feature_engineering.py


## Step 7 – Verify PostgreSQL Data

psql -h localhost -U postgres -d cdp
SELECT * FROM loan_transactions;


