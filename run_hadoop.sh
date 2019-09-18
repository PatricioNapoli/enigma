#!/bin/bash

docker-compose -p enigma-hadoop -f hadoop/docker-compose.yml up -d --build
