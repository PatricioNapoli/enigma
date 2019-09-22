#!/bin/bash

docker rm gatherer -f
docker run --name gatherer --network=enigma gatherer:latest
