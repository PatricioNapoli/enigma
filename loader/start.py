from pyspark.sql.types import *
from pydoop import hdfs

from pyspark.context import SparkContext
from pyspark import SparkConf
from pyspark.sql.session import SparkSession

import json

if __name__ == "__main__":
    print("Initializing Parquet loader.")

    fs = hdfs.hdfs(host="hadoop", port=8020, user="root")

    conf = SparkConf().setMaster('spark://spark-master:7077')
    sc = SparkContext(conf=conf)
    spark = SparkSession(sc)

    cass_options = {"spark.cassandra.connection.host": 'cassandra', "table": "crypto", "keyspace": "enigma"}

    for path in fs.list_directory("/user/root/parquet"):
        df = spark.read.parquet(path_name)

        df.write.format("org.apache.spark.sql.cassandra")
                .mode('append')
                .options(**cass_options)
                .save()

    # TODO
