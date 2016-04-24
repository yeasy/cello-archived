#!/bin/bash

BIND_ADDR=0.0.0.0
#BIND_ADDR=127.0.0.1

echo "Access port 8081 for the mongo-express UI".

docker run -it --rm \
    --link poolmanager_mongo_1:mongo \
    --net poolmanager_default \
    -p ${BIND_ADDR}:8081:8081 \
    mongo-express:0.30

