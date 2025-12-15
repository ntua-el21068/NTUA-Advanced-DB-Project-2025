import os
import sys
import subprocess
from pyspark.sql import SparkSession

# --- 1. GLOBAL DATA CONSTANTS ---
BASE_S3 = "s3a://initial-notebook-data-bucket-dblab-905418150721/project_data"

CRIME_DATA = [
    f"{BASE_S3}/LA_Crime_Data/LA_Crime_Data_2010_2019.csv",
    f"{BASE_S3}/LA_Crime_Data/LA_Crime_Data_2020_2025.csv"
]
STATIONS_DATA = f"{BASE_S3}/LA_Police_Stations.csv"
MO_CODES_DATA = f"{BASE_S3}/MO_codes.txt"
RE_CODES_DATA = f"{BASE_S3}/RE_codes.csv"

# --- 2. CONFIGURATION FUNCTION ---
def get_spark_session(app_name="AdvancedDB_Project", executors="4", cores="1", memory="2g"):
    """
    Initializes Spark with Java 8, AWS S3, and Sedona.
    Defaults to 4 executors 
    """
    print(f"Configuring Environment for '{app_name}'...")
    print(f"   Resource Config: {executors} Executors | {cores} Cores | {memory} RAM")
    
    # A. Java Fix
    try:
        java_path = subprocess.check_output(["which", "java"]).decode().strip()
        if os.path.islink(java_path):
            java_path = os.path.realpath(java_path)
        java_home = os.path.dirname(os.path.dirname(java_path))
        os.environ["JAVA_HOME"] = java_home
        if 'PYSPARK_SUBMIT_ARGS' in os.environ:
             del os.environ['PYSPARK_SUBMIT_ARGS']
        print(f"   JAVA_HOME set to: {java_home}")
    except Exception as e:
        print(f"   Java Warning: {e}")

    # B. Packages 
    sedona_ver = "1.6.1"
    geotools_ver = "1.6.1-28.2"
    packages = [
        f"org.apache.sedona:sedona-spark-shaded-3.4_2.12:{sedona_ver}",
        f"org.datasyslab:geotools-wrapper:{geotools_ver}",
        "org.apache.hadoop:hadoop-aws:3.3.2"
    ]
    os.environ['PYSPARK_SUBMIT_ARGS'] = f"--packages {','.join(packages)} pyspark-shell"

   # C. Build Session
    spark = (SparkSession.builder 
        .appName(app_name) 
        .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer") 
        .config("spark.kryo.registrator", "org.apache.sedona.core.serde.SedonaKryoRegistrator") 
        .config("spark.kryoserializer.buffer.max", "512m")  
        .config("spark.sql.extensions", "org.apache.sedona.sql.SedonaSqlExtensions") 
        .config("spark.executor.instances", executors) 
        .config("spark.executor.cores", cores)      
        .config("spark.executor.memory", memory)    
        .config("spark.driver.memory", "4g") 
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") 
        .config("spark.hadoop.fs.s3a.aws.credentials.provider", "com.amazonaws.auth.InstanceProfileCredentialsProvider,com.amazonaws.auth.DefaultAWSCredentialsProviderChain") 
        .getOrCreate()
    )
    
    # D. Initialize Sedona 
    try:
        from sedona.spark import SedonaContext
        spark = SedonaContext.create(spark)
        print("   Sedona Context Active")
    except ImportError:
        print("   Sedona library not found.")
    except Exception as e:
        print(f"   Sedona Init Error: {e}")
        
    return spark