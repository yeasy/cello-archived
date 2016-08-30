#!/usr/bin/env bash

echo "Pull yeasy/hyperledger:0.5-dp and retagging"
docker pull yeasy/hyperledger:0.5-dp && \
docker rmi hyperledger/fabric-baseimage:latest && \
docker tag yeasy/hyperledger:0.5-dp hyperledger/fabric-baseimage:latest

echo "Pull yeasy/hyperledger-peer:0.5-dp"
docker pull yeasy/hyperledger-peer:0.5-dp && \
docker tag yeasy/hyperledger-peer:0.5-dp yeasy/hyperledger-peer:latest
