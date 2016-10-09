# Deployment

**Hyperledger fabric changes the service port number since 0.6, so if you want to use the legacy 0.5 code, please use the dp-0.5 branch.**

There are two kinds of nodes, we suggest all nodes are Linux-based (Ubuntu 14.04+) VM/Servers: 

* Master Node: run the management service, to operate the chains in Work Nodes;
* Worker Node: serve as chain hosts.

In this doc, we describe how to setup the Master node.

## Config System
Please first read and meet the [System Requirement](system_requirement.md).


## Clone Code

```sh
$ sudo aptitude install git make -y
$ git clone https://github.com/yeasy/cello && cd cello
```

##  Setup

For the first time running, please setup the master node with

```sh
$ make setup
```

## Usage

To (re)start the whole services, please run

```sh
$ make restart
```

To (re)deploy one sub service, e.g., dashboard, please run

```sh
$ make redeploy service=watchdog
```

To check the logs for the services, please run

```sh
$ make logs
$ make log service=watchdog
```

## Configuration
The application configuration can be imported from file named `CELLO_CONFIG_FILE`.

By default, it also loads the `config.py` file as the configurations.

Configuration can be set through following environment variables in the [docker-compose.yml](docker-compose.yml):

* `MONGO_URL=mongodb://mongo:27017`
* `MONGO_COLLECTION=dev`
* `DEBUG=True`

## Data Storage
The mongo container will use local `/opt/cello/mongo` directory for persistent storage. 

Please keep it safe by backups or using more high-available solutions.

## Production Consideration

* Use the code from `release` branch.
* Configuration: Set all parameters to production, including image, compose, and application.
* Security: Use firewall to filter traffic, enable TLS and authentication.
* Backup: Enable automatic data backup.
* Monitoring: Enable monitoring services.
