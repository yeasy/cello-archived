#!/usr/bin/env bash

# This script will start all services using docker-compose.
# It should be triggered at the upper directory

DB_DIR=/opt/poolmanager/mongo

echo "Checking Docker-engine..."
command -v docker >/dev/null 2>&1 || { echo >&2 "I require docker-engine>=1.8.0 but it's not installed.  Aborting."; exit 1; }

echo "Checking Docker-compose..."
command -v docker-compose >/dev/null 2>&1 || { echo >&2 "I require docker-compose>=1.7.0 but it's not installed.  Aborting."; exit 1; }

echo "Checking local for mounted database path..."
[ ! -d ${DB_DIR} ] && echo "Local database path not existed, creating one" && mkdir -p ${DB_DIR}

[ `docker ps -qa|wc -l` -gt 0 ] && echo "Warn: existing containers may cause unpredictable failure"

echo "Start all services..."
docker-compose up -d --no-recreate