# PoolManager

Manager who maintains a pool of hyperledger cluster.

The rest API will be called by web service backend.

* [Terminology](docs/terminology.md)
* [API usage](docs/api.md)
* [Architecture Design](docs/arch.md)

## Installation

### Master
* docker>=1.9.0.
* docker images: python:3.5, mongo:3.2, yeasy/nginx,

### Node
TODO: need a setup script.

* docker: >=1.9.0, and open daemon 2735 port for Master.
* docker images: yeasy/hyperledger (rename to openblockchain/baseimage),
yeasy/hyperledger-peer,
yeasy/hyperledger-membersrvc
* SSH: May open for Master to monitor

## Dependency

* docker-py >= 1.8.0
* docker-compose >= 1.7.0