# Enigma

Gathers historical price data from a Cryptocurrency database, cleans it and loads it into HDFS. Afterwards, it is schematized into a parquet file using Apache Spark. Then it is loaded into a Cassandra database. Finally, it is analyzed and generates charts from analysis.

# Install
Install docker and docker-compose in your machine.

# Running
Run ./setup.sh
Run hadoop, cassandra and spark .sh scripts.

# Batch Process Steps
1. Run gatherer
2. Run schema
3. Run loader
4. Run analytics
5. Run report
