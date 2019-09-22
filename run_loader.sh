#!/bin/bash

docker rm loader -f
docker run --name loader --network=enigma -v enigma_ivy_cache:/root/.ivy2 loader:latest
