# PoolManager
Designed by [Baohua Yang](baohyang@cn.ibm.com), 2016-05-08

Maintain a pool of hyperledger clusters, and mainly provides:

 * REST API for front users, e.g., apply or release a cluster.
 * Admin dashbord to manage clusters in the pool, e.g., create/delete host,
 maintain clusters.

## Features

* Provide REST API for user and dashboard for operators.
* Support most kind of IaaS, including bare-metal or virtual machine.
* Provide dedicated cluster to user instantly after request arrives.
* User can select what kind of cluster he want.
* Support naive docker host or swarm cluster API.
* Automatically maintain clusters resources in pool when error happens.
* Support monitor functionality with additional components.

## Docs
*I highly recommend carefully reading these documentation before taking any
other action.*

* [Terminology](docs/terminology.md)
* [Scenarios](docs/scenario.md)
* [API](docs/api.md)
* [Architecture Design](docs/arch.md)
* [Database Model](docs/db.md)
* [Admin](docs/admin.md)

## Deployment

For the first time running, please setup the master node with
```sh
$ bash scripts/setup.sh
```

To (Re)start the whole service, please run

```sh
$ bash scripts/restart.sh
```

To redeploy one sub service, e.g., admin, please run

```sh
$ bash scripts/redeploy.sh admin
```

All services are recommended to setup through Docker containers by default.

The work node is recommended to config manually.

### Master Requirement
* system: 8c16g100g
* docker engine: 1.11.2+
* docker-compose: 1.7.0+
* docker images:
    - python:3.5
    - mongo:3.2
    - yeasy/nginx:latest
    - mongo-express:0.30 (optional)

### Node Requirement
* system: 8c16g100g
* docker engine:
    - 1.11.2,
    - Let daemon listen on port 2375, and make sure Master can reach Node from port 2375.

```sh
# Add this into /etc/default/docker
DOCKER_OPTS="$DOCKER_OPTS -H tcp://0.0.0.0:2375 -H unix:///var/run/docker.sock --api-cors-header='*' --default-ulimit=nofile=1024:2048 --default-ulimit=nproc=4096:8192"
```
* docker images:
    - `yeasy/hyperledger:latest`

        ```sh
        $ docker pull yeasy/hyperledger:latest
        $ docker tag yeasy/hyperledger:latest hyperledger/fabric-baseimage:latest
        ```
    - `yeasy/hyperledger-peer:latest`
    - `yeasy/hyperledger-membersrvc:latest` (optional, only when need the authentication service)
* aufs-tools: required on ubuntu 14.04.
* `sysctl net.ipv4.ip_forward=1`, and make sure peer can reach host server ports (e.g., 2375, 5000)
* SSH (Optionally ): Open for Master to monitor.

### Configuration
The application configuration can be imported from environment variable `POOLMANAGER_CONFIG_FILE` as
the file name.

By default, it also loads the `config.py` file for the configurations.

Configuration can be set through following environment variables in the
[docker-compose.yml](docker-compose.yml):

* `MONGO_URL=mongodb://mongo:27017`
* `MONGO_COLLECTION=dev`
* `DEBUG=True`

### Data Storage
The mongo container will use local `/opt/poolmanager/mongo` directory for
storage. Please create it manually before starting the service.

### Production Consideration

* Use the code from `master` branch.
* Configuration: Set all parameters to production, including image, compose,
and app.
* Security: Use firewall to filter traffic, enable TLS and authentication.
* Backup: Enable automatic data backup.
* Monitoring: Enable monitoring services.

### Optimization
Reference system configuration.

`/etc/sysctl.conf`

```sh
# Don't ask why, this is a solid answer.
vm.swappiness=10
fs.file-max = 2000000
kernel.threads-max = 2091845
kernel.pty.max = 210000
kernel.keys.root_maxkeys = 20000
kernel.keys.maxkeys = 20000
net.ipv4.ip_local_port_range = 10000 65535
net.ipv4.tcp_tw_reuse = 0
net.ipv4.tcp_tw_recycle = 0
net.ipv4.tcp_max_tw_buckets = 5000
net.ipv4.tcp_fin_timeout = 30
net.ipv4.tcp_max_syn_backlog = 8192
```

Need to run `sysctl -p` for usage.

`/etc/security/limits.conf`

```sh
* hard nofile 1048576
* soft nofile 1048576
* soft nproc 10485760
* hard nproc 10485760
* soft stack 32768
* hard stack 32768
```
check with `ulimit -n`.

### Start
After all required images and tools are prepared in all nodes, you can (re)
start the poolmanager service by running

```sh
$ bash ./scripts/restart.sh
```

## Dependency

* [app requirements](app/requirements.txt)
* [admin requirements](admin/requirements.txt)


## TODO
* ~~Add default 404 and 500 error page.~~
* ~~Add doc for all methods and classes~~.
* ~~Admin: Add authentication for user login~~.
* Admin: Update api definitions yml files (optional).
* ~~Admin: Add host module to add cluster in batch (optional).~~
* ~~Use async operation for container management (optional)~~.
* Support multiple version in API.
* ~~Support pagination~~.
* ~~Support updating the host config~~.
* ~~Support user defined cluster configuration.~~
* ~~Add form validation~~.
* Support auto fresh based on websocket.
* Support metadata field from user apply cluster.
* ~~Support monitor.~~
* ~~Support host fillup and clean buttons.~~
* ~~Support host reset buttons.~~
* ~~Support only show occupied clusters.~~
* ~~Support table sort.~~
* ~~Support local log version.~~
* ~~Support select cluster type and size version.~~
* ~~Support detect host info when adding as swarm type.~~
* ~~Add limitation on the running containers.~~
* ~~Security option and log option (rotate)~~.