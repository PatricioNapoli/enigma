#!/bin/bash

docker-compose -p enigma-services -f services/docker-compose.yml up -d --build
