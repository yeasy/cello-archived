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

echo "Checking local Docker image..."
[[ "$(docker images -q mongo:3.2 2> /dev/null)" == "" ]] && echo "Mongo:3.2 is not there, may use some time to pull it down for the first time running"
[[ "$(docker images -q python:3.5 2> /dev/null)" == "" ]] && echo "Python:3.5 is not there, may use some time to pull it down for the first time running"

[ `docker ps -qa|wc -l` -gt 0 ] && echo "Warn: existing containers may cause unpredictable failure"

echo "Start all services..."
docker-compose up -d --no-recreate