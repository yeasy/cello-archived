# System Requirement

You may need to install `git` and `make` manually before cloning the code and using the setup scripts. 

## Master Node
* Hardware: 8c16g100g
* Docker engine: 1.11.2+
* Docker images:
    - python:3.5
    - mongo:3.2
    - yeasy/nginx:latest
    - mongo-express:0.30 (optional)
* docker-compose: 1.7.0+

Please see [Deployment](deployment.md) setup part to see how to install those tools.

## Worker Node
* Hardware: 8c16g100g
* `sysctl -w net.ipv4.ip_forward=1`, and make sure host ports are open (e.g., 2375, 7050~10000)
* Docker engine:
    - 1.12.0+ (1.11.2 for 0.5-dp branch).
    - Let daemon listen on port 2375, and make sure Master can reach Worker Node through this port.
    - Config Docker daemon as the following:
```sh
# Add this into /etc/default/docker
DOCKER_OPTS="$DOCKER_OPTS -H tcp://0.0.0.0:2375 -H unix:///var/run/docker.sock --api-cors-header='*' --default-ulimit=nofile=8192:16384 --default-ulimit=nproc=8192:16384"
```
* Docker images:

    *To use specific version fabric code, then mark corresponding tag when pulling, e.g., `yeasy/hyperledger-fabric:0.6-dp` tag for 0.6-dp release.*
    - `yeasy/hyperledger-fabric:latest`
        ```sh
        $ docker pull yeasy/hyperledger-fabric:latest
        $ docker tag yeasy/hyperledger-fabric:latest hyperledger/fabric-peer:latest
        $ docker tag yeasy/hyperledger-fabric:latest hyperledger/fabric-baseimage:latest
        $ docker tag yeasy/hyperledger-fabric:latest hyperledger/fabric-membersrvc:latest # (optional, only when need the authentication service)
        ```
* aufs-tools (optional): Only required on ubuntu 14.04.

## System Optimization
Reference system configuration.

### `/etc/sysctl.conf`

```sh
# Don't ask why, this is a solid answer.
vm.swappiness=10
fs.file-max = 2000000
kernel.threads-max = 2091845
kernel.pty.max = 210000
kernel.keys.root_maxkeys = 20000
kernel.keys.maxkeys = 20000
net.ipv4.ip_local_port_range = 30000 65535
net.ipv4.tcp_tw_reuse = 0
net.ipv4.tcp_tw_recycle = 0
net.ipv4.tcp_max_tw_buckets = 5000
net.ipv4.tcp_fin_timeout = 30
net.ipv4.tcp_max_syn_backlog = 8192
```

Then, need to run `sysctl -p` for enabling.

### `/etc/security/limits.conf`

```sh
* hard nofile 1048576
* soft nofile 1048576
* soft nproc 10485760
* hard nproc 10485760
* soft stack 32768
* hard stack 32768
```
Logout and login, then check with `ulimit -n`.