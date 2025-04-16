import sys
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.types import StructType, StructField, StringType, TimestampType

# Glue boilerplate
glueContext = GlueContext(SparkContext())
spark = glueContext.spark_session
job = Job(glueContext)
job.init('etl-user-activity', args={})

# Step 1: Define schema for nested JSON
schema = StructType([
    StructField("user_id", StringType(), True),
    StructField("action", StringType(), True),
    StructField("timestamp", StringType(), True),
    StructField("metadata", StructType([
        StructField("ip", StringType(), True),
        StructField("device", StringType(), True)
    ]))
])

# Step 2: Read with schema
df = spark.read.schema(schema).json("s3://user-activity-logs-naz/raw/")

# Step 3: Flatten nested metadata
flat_df = df.select(
    "user_id",
    "action",
    "timestamp",
    "metadata.ip",
    "metadata.device"
)

# Step 4: Register view for SQL query (now safe)
flat_df.createOrReplaceTempView("new")

# Step 5: Aggregate query
summary_df = spark.sql("""
  SELECT action, COUNT(*) as count
  FROM new
  GROUP BY action
""")

# Step 6: Write output to S3
summary_df.write \
    .mode("overwrite") \
    .option("header", "true") \
    .csv("s3://user-activity-logs-naz/processed/")

# Finish job
job.commit()

