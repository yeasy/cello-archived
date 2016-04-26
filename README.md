# PoolManager

Manager who maintains a pool of hyperledger cluster, and provides rest API
for other front end services.

## docs
I highly recommend carefully reading these documentation before taking any
other action.

* [Terminology](docs/terminology.md)
* [API](docs/api.md)
* [Architecture Design](docs/arch.md)

## Deployment

### Master
* docker>=1.9.0.
* docker images: python:3.5, mongo:3.2, yeasy/nginx,

### Node
TODO: We may need a setup script.

* docker: >=1.9.0, and open daemon port 2375 for Master usage.
* docker images: yeasy/hyperledger (rename to openblockchain/baseimage),
yeasy/hyperledger-peer,
yeasy/hyperledger-membersrvc
* SSH: May open for Master to monitor

### Prodution consideration

* Mode: Set all modes to production, including image, compose, and app.
* Security: Use firewall to filter traffic, enable TLS and authentication.
* Monitoring: Enable monitoring services.
* Backup: Enable automatic data backup.

## Dependency

There are 3 main dependencies:

* docker-py >= 1.8.0
* docker-compose >= 1.7.0
* python >= 3.0

Details, see [requirements.txt](requirements.txt)

## TODO
* Add default 404 and 500 error page.
* Add doc for most methods and classes.
* Use async operation for docker container management (maybe not necessary).
