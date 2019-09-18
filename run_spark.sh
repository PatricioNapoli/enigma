#!/bin/bash

docker-compose -p enigma-spark -f spark/docker-compose.yml up -d --build
