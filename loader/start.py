from pyspark.sql.types import *
from pydoop import hdfs

from pyspark.context import SparkContext
from pyspark import SparkConf
from pyspark.sql.session import SparkSession

import json

if __name__ == "__main__":
    print("Initializing Parquet schematizer.")

    fs = hdfs.hdfs(host="hadoop", port=8020, user="root")

    conf = SparkConf().setMaster('spark://spark-master:7077')
    sc = SparkContext(conf=conf)
    spark = SparkSession(sc)

    # TODO
