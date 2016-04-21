#!/usr/bin/env bash

# This script will only build and redeploy the app container.
# It should be triggered at the upper directory

echo "Building the poolmanager image"
docker-compose build manager

echo "Redeploy the manager container"
docker-compose up --no-deps -d manager