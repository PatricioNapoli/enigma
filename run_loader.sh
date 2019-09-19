#!/bin/bash

docker rm loader -f
docker run --name loader --network=enigma loader:latest
