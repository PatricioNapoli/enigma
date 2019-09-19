from pyspark.sql.types import *
from pydoop import hdfs

from pyspark.context import SparkContext
from pyspark import SparkConf
from pyspark.sql.session import SparkSession

import json

if __name__ == "__main__":
    print("Initializing Parquet loader.")

    fs = hdfs.hdfs(host="hadoop", port=8020, user="root")

    conf = SparkConf().set("spark.cassandra.connection.host", "cassandra").setMaster('spark://spark-master:7077')
    sc = SparkContext(conf=conf)
    spark = SparkSession(sc)

    for path in fs.list_directory("/user/root/parquet"):
        path_name = path["path"]

        df = spark.read.parquet(path_name)

        file_name = path_name.split("/")[-1]

        # First 3 characters is coin
        table = file_name[:3]

        df.write.format("org.apache.spark.sql.cassandra").mode('append').options(table=table.lower(), keyspace="enigma").save()

    print("Finished loading to cassandra.")        
