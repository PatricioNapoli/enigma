from pyspark.sql.types import *

from pyspark.context import SparkContext
from pyspark import SparkConf
from pyspark.sql.session import SparkSession

import json

coins = ['btc', 'eth']

if __name__ == "__main__":
    print("Initializing analytics.")

    fs = hdfs.hdfs(host="hadoop", port=8020, user="root")

    conf = SparkConf().set("spark.cassandra.connection.host", "cassandra").setMaster('spark://spark-master:7077')
    sc = SparkContext(conf=conf)
    spark = SparkSession(sc)

    for coin in coins:
        df = spark.read.format("org.apache.spark.sql.cassandra").options(table=coin, keyspace='enigma').load()

    print("Finished analytics.")
