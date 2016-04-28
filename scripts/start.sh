#!/usr/bin/env bash

# This script will start all services using docker-compose.
# It should be triggered at the upper directory

echo "Checking environment..."
[ `docker ps -qa|wc -l` -gt 0 ] && echo "Warn: existing containers may cause
 unpredictable failure"

echo "Start all services..."
docker-compose up -d --no-recreate