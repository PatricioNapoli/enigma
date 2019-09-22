#!/bin/bash

docker build -t python-hadoop .
docker build -t gatherer:latest gatherer/
docker build -t schema:latest schema/
docker build -t loader:latest loader/
docker build -t analytics:latest analytics/