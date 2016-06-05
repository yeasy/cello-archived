#!/bin/bash
# NOT run this in production environment.
# This script will start a mongo-express node for debugging.
# It should be triggered at the upper directory

BIND_ADDR=0.0.0.0
#BIND_ADDR=127.0.0.1

echo "Access port 8081 for the mongo-express UI"

docker run -it --rm \
    --link mongo:mongo \
    --net poolmanager_default \
    -p ${BIND_ADDR}:8081:8081 \
    -e ME_CONFIG_BASICAUTH_USERNAME=admin \
    -e ME_CONFIG_BASICAUTH_PASSWORD=pass \
    mongo-express:0.30

