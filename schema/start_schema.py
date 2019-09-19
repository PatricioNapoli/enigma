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

    current_processed = []

    for path in fs.list_directory("/user/root/parquet"):
        current_processed.append(path["path"].split("/")[-1].replace(".parquet", ""))

    for path in fs.list_directory("/user/root/"):
        path_name = path["path"]
        file_name = path_name.split("/")[-1]

        if ".json" not in file_name:
            continue

        if file_name in current_processed:
            continue

        df = spark.read.json(path_name)

        hdfs_path = f"hdfs://hadoop:8020/user/root/parquet/{file_name}.parquet"

        print(f"Schematizing {path_name} to {hdfs_path}")
        df.write.format('parquet').save(hdfs_path)

    print("Finished schematizing.")
