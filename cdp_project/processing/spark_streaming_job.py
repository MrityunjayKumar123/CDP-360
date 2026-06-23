# processing/spark_streaming_job.py

import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

hadoop_home = "D:/MJ/CDP-360-main/CDP-360-main/cdp_project"
os.environ["HADOOP_HOME"] = hadoop_home
os.environ["PATH"] = f"{hadoop_home}/bin;{os.environ.get('PATH', '')}"

spark = SparkSession.builder \
    .appName("CDPStreaming") \
    .master("local[*]") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.13:4.1.2") \
    .config("spark.jars.excludes", "com.google.code.findbugs:jsr305") \
    .config("spark.sql.streaming.forceDeleteTempCheckpointLocation", "true") \
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

# Write to PostgreSQL
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
