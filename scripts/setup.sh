#!/usr/bin/env bash

# This script will try setup a valid environment for the docker-compose running.

## DO NOT MODIFY THE FOLLOWING PART, UNLESS YOU KNOW WHAT IT MEANS ##
echo_r () {
    [ $# -ne 1 ] && return 0
    echo -e "\033[31m$1\033[0m"
}
echo_g () {
    [ $# -ne 1 ] && return 0
    echo -e "\033[32m$1\033[0m"
}
echo_y () {
    [ $# -ne 1 ] && return 0
    echo -e "\033[33m$1\033[0m"
}
echo_b () {
    [ $# -ne 1 ] && return 0
    echo -e "\033[34m$1\033[0m"
}

pull_image() {
    [ $# -ne 1 ] && return 0
    name=$1
    [[ "$(docker images -q mongo:3.2 2> /dev/null)" == "" ]] && echo_r "Not found ${name}, may need some time to pull it down..." && docker pull ${name}
}

USER="opuser"

DB_DIR=/opt/poolmanager/mongo

apt-get update && apt-get install -y -m curl docker-engine python-pip

pip install --upgrade pip

echo "Checking Docker-engine..."
command -v docker >/dev/null 2>&1 || { echo_r >&2 "No docker-engine found, try installing"; curl -sSL https://get.docker.com/ | sh; service docker restart; }

echo "Add existing user to docker group"
usermod -aG docker ${USER}

echo "Checking Docker-compose..."
command -v docker-compose >/dev/null 2>&1 || { echo_r >&2 "No docker-compose found, try installing"; pip install -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com docker-compose; }

echo "Checking local for mounted database path..."
[ ! -d ${DB_DIR} ] && echo_r "Local database path not existed, creating one" && mkdir -p ${DB_DIR} && chown -R ${USER}:${USER} ${DB_DIR}

echo "Checking local Docker image..."
pull_image "mongo:3.2"
pull_image "python:3.2"
pull_image "yeasy/nginx:latest"

[ `docker ps -qa|wc -l` -gt 0 ] && echo_r "Warn: existing containers may cause unpredictable failure"

echo_g "Please logout and login again to enable the setup."
echo_g "It's safe to run this script repeatedly. Just re-run if the setup fails."
