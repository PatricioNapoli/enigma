#!/bin/bash

docker build -t python-hadoop .
docker build -t gatherer:latest gatherer/
docker build -t schema:latest schema/
