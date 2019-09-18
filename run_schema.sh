#!/bin/bash

docker rm schema -f
docker run --name schema --network=enigma schema:latest
