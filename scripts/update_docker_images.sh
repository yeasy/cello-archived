#!/usr/bin/env bash

echo "Pull yeasy/hyperledger:latest and renaming"
docker pull yeasy/hyperledger:latest && \
docker rmi hyperledger/fabric-baseimage:latest && \
docker tag yeasy/hyperledger:latest hyperledger/fabric-baseimage:latest

echo "Pull yeasy/hyperledger-peer:latest"
docker pull yeasy/hyperledger-peer:latest
