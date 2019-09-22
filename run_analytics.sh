#!/bin/bash

docker rm analytics -f
docker run --name analytics --network=enigma -v enigma_analytics_data:/usr/schema/out -v enigma_ivy_cache:/root/.ivy2 analytics:latest
