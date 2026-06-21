# processing/spark_streaming_job.py

from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = SparkSession.builder \
    .appName("CDPStreaming") \
    .getOrCreate()

# Read from Kafka
df = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "loan.applications") \
    .load()

# Parse JSON
parsed = df.selectExpr("CAST(value AS STRING) as json") \
    .selectExpr("from_json(json, 'loan_id STRING, customer_id STRING, status STRING, timestamp STRING') as data") \
    .select("data.*")

# Write Bronze → Delta Lake
parsed.writeStream.format("delta") \
    .option("checkpointLocation", "/tmp/delta/checkpoints/bronze") \
    .option("path", "/tmp/delta/bronze") \
    .outputMode("append") \
    .start()

# Simultaneous write to PostgreSQL (operational fields)
parsed.writeStream \
    .foreachBatch(lambda batch_df, _: batch_df.write \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://localhost:5432/cdp") \
        .option("dbtable", "loan_transactions") \
        .option("user", "postgres") \
        .option("password", "password") \
        .save()) \
    .start() \
    .awaitTermination()
