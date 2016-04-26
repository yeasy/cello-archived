#!/usr/bin/env bash

# This script will only build and redeploy the specific service.
# It should be triggered at the upper directory

if [ "$#" -ne 1 ]; then
    echo "give service name as arguments, e.g., app, admin"
    exit
fi

SERVICE=$1

echo "Remove the container and image"
docker-compose stop ${SERVICE}
docker-compose rm -f --all ${SERVICE}
docker rmi poolmanager-${SERVICE}

echo "Building the poolmanager-${SERVICE} image"
docker-compose build ${SERVICE}


echo "Redeploy the poolmanager-${SERVICE} container"
docker-compose up --no-deps -d ${SERVICE}