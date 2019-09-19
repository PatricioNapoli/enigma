#!/bin/sh

spark-submit --packages datastax:spark-cassandra-connector:2.4.0-s_2.11 start_analytics.py
