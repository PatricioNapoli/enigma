#!/bin/bash

docker rm enigma -f
docker run --name enigma --network=enigma gatherer:latest
