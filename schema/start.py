from pyspark.sql.types import *
from pydoop import hdfs

from pyspark.context import SparkContext
from pyspark.sql.session import SparkSession

import json

if __name__ == "__main__":
    print("Initializing Parquet schematizer.")

    fs = hdfs.hdfs(host="hadoop", port=8020, user="root")

    sc = SparkContext.getOrCreate()
    spark = SparkSession(sc)

    for path in fs.list_directory("/user/root/"):
        path_name = path["path"]

        print(path_name)
        df = spark.read.json(path_name)
        
        file_name = path_name.split("/")[-1]
        df.write.format('parquet').save(f"hdfs://hadoop:8020/user/root/parquet/{file_name}.parquet")
