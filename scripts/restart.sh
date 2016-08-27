#!/usr/bin/env bash

# This script will check the env and (re)start all services.
# It should be triggered at the upper directory, and safe to repeat.

source ./header.sh

DB_DIR=/opt/${PROJECT}/mongo

echo_b "Checking Docker-engine..."
command -v docker >/dev/null 2>&1 || { echo >&2 "I require docker-engine>=1.8.0 but it's not installed.  Aborting."; exit 1; }

echo_b "Checking Docker-compose..."
command -v docker-compose >/dev/null 2>&1 || { echo >&2 "I require docker-compose>=1.7.0 but it's not installed.  Aborting."; exit 1; }

echo_b "Checking local for mounted database path..."
[ ! -d ${DB_DIR} ] && echo "Local database path not existed, creating one" && mkdir -p ${DB_DIR}

echo_b "Checking local Docker image..."
[[ "$(docker images -q mongo:3.2 2> /dev/null)" == "" ]] && echo "Mongo:3.2 is not there, may use some time to pull it down for the first time running"
[[ "$(docker images -q python:3.5 2> /dev/null)" == "" ]] && echo "Python:3.5 is not there, may use some time to pull it down for the first time running"

[ `docker ps -qa|wc -l` -gt 0 ] && echo_r "Warn: existing containers may cause unpredictable failure"

echo_b "Stop all services..."
docker-compose stop

echo_b "Remove all services..."
docker-compose rm -f -all

echo_b "Restart all services..."
docker-compose up -d --no-recreate

#echo "Restarting mongo_express"
#[[ "$(docker ps -q --filter='name=mongo_express')" != "" ]] && docker restart mongo_express