#!/usr/bin/env bash

# This script will (re)start all services.
# It should be triggered at the upper directory, and safe to repeat.

source ./header.sh

echo_b "Stop all services..."
docker-compose stop

echo_b "Remove all services..."
docker-compose rm -f -all

echo_b "Restart all services..."
docker-compose up -d --no-recreate

#echo "Restarting mongo_express"
#[[ "$(docker ps -q --filter='name=mongo_express')" != "" ]] && docker restart mongo_express