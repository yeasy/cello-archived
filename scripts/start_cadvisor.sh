#!/usr/bin/env bash


echo "Pull yeasy/hyperledger:latest"
docker pull yeasy/hyperledger:latest

echo "Renaming"
docker rmi hyperledger/fabric-baseimage:latest
docker tag yeasy/hyperledger:latest hyperledger/fabric-baseimage:latest

echo "Pull yeasy/hyperledger-peer:noops"
docker pull yeasy/hyperledger-peer:noops

echo "Pull yeasy/hyperledger-peer:pbft"
docker pull yeasy/hyperledger-peer:pbft
