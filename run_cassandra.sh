#!/bin/bash

docker-compose -p enigma-cassandra -f cassandra/docker-compose.yml up -d --build
