from pyspark.sql import SparkSession
from pyspark.sql.types import StringType,StructField,IntegerType,FloatType,StructType
from configurations import configuration
from pyspark.sql.functions import from_json,col
import os

def initialize_spark():
    
    spark=SparkSession.builder.appName("Realtime Data Streaming Piepline")\
        .config('spark.jars.packages',
                    'org.apache.spark:spark-sql-kafka-0-10_2.13:3.5.0,'
                    'org.apache.hadoop:hadoop-aws:3.3.1,'
                    'com.amazonaws:aws-java-sdk:1.11.469')\
        .config('spark.hadoop.fs.s3a.impl','org.apache.hadoop.fs.s3a.S3AFileSystem')\
        .config('spark.hadoop.fs.s3a.access.key', configuration.get('AWS_ACCESS_KEY'))\
        .config('spark.hadoop.fs.s3a.secret.key', configuration.get('AWS_SECRET_KEY'))\
        .config('spark.hadoop.fs.s3a.aws.credentials.provider', 
                'org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider')\
        .getOrCreate()
        
    return spark

def spark_consumer(spark,KAFKA_BOOTSTRAP_SERVERS,topic):
    # try:
    #     df=spark.readStream.format("kafka").option("kafka.bootstrap.servers",KAFKA_BOOTSTRAP_SERVERS).option("subscribe",topic).option("startingOffsets","earliest").load()
    #     print("Streaming Consumed successfully")
    #     return df
    # except:
    #     print("Streaming Failed")
    #     return None
    df = spark \
            .readStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS) \
            .option("subscribe", topic) \
            .option("startingOffsets", "earliest") \
            .load()
    print("Streaming Consumed successfully")
    return df
    
    
def transform_streaming_data(df):
    schema = StructType([
        StructField("name", StringType(), True),
        StructField("gender", StringType(), True),
        StructField("address", StringType(), True),
        StructField("city", StringType(), True),
        StructField("nation", StringType(), True),
        StructField("zip", StringType(), True),
        StructField("latitude", FloatType(), True),
        StructField("longitude", FloatType(), True),
        StructField("email", StringType(), True)
    ])

    transformed_df = df.selectExpr("CAST(value AS STRING)") \
                       .select(from_json(col("value"), schema).alias("data")) \
                       .select("data.*")

    return transformed_df

def upload_to_s3(df,path,checkpoint_location):
    
    query= (df.writeStream.format('parquet').option('checkpointLocation', checkpoint_location)\
                .option('path', path).outputMode('append').start())
    
    query.awaitTermination()
    


def main():
    
    KAFKA_BOOTSTRAP_SERVERS = 'kafka1:9092'
    KAFKA_TOPIC = 'Dataingestion_topic'
    path='s3a://realtimedatastreamingpipelinebucket/data'
    checkpoint_location='s3a://realtimedatastreamingpipelinebucket/checkpoint'
    
    spark=initialize_spark()
    if spark:
        df=spark_consumer(spark,KAFKA_BOOTSTRAP_SERVERS,KAFKA_TOPIC)
        if df:
            tranformed_df=transform_streaming_data(df)
            print(tranformed_df)
            #tranformed_df.show(10,truncate=False)
            #query= tranformed_df.writeStream \
            #    .format('console').outputMode('append').start()
            upload_to_s3(tranformed_df,path,checkpoint_location)
            
            
            
if __name__=='__main__':
    main()