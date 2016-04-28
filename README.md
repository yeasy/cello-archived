# PoolManager

Manager who maintains a pool of hyperledger clusters, and mainly provides:

 * REST API for front end services, e.g., apply or release a cluster.
 * Admin dashbord to manage clusters in the pool, e.g., create,
 delete and query the cluster.

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

### Master
* docker engine: >=1.9.0.
* docker-py: >= 1.8.0
* docker-compose: >=1.7.0.
* docker images: python:3.x, mongo:3.2, yeasy/nginx

### Node

*TODO: We may need a setup script.*

* docker engine: >=1.9.0, and open daemon port 2375 for Master usage.
* docker images:
    - yeasy/hyperledger (After pulling, rename to openblockchain/baseimage)
    - yeasy/hyperledger-peer (match with the [compose](admin/common/compose-defaults.yml) file)
    - yeasy/hyperledger-membersrvc (optional, only when need the authentication service)
* SSH (Optionally ): Open for Master to monitor.

### Configuration
The application configuration can be imported from environment variable `POOLMANAGER_CONFIG_FILE` as
the file name.

By default, it also loads the `config.py` file for the configurations.

Database can be set through following environment variables:

* `MONGO_URL=mongodb://mongo:27017`
* `MONGO_COLLECTION=dev`

### Data Storage
The mongo container will use local `/opt/poolmanager/mongo` directory for
storage. Please create it manually before starting the service.

### Production Consideration

* Configuration: Set all parameters to production, including image, compose,
and app.
* Security: Use firewall to filter traffic, enable TLS and authentication.
* Backup: Enable automatic data backup.
* Monitoring: Enable monitoring services.

## Dependency

* [app requirements](app/requirements.txt)
* [admin requirements](admin/requirements.txt)


## TODO
* ~~Add default 404 and 500 error page.~~
* ~~Add doc for all methods and classes~~.
* Admin: Add manual release button.
* Admin: Update api definitions in yml files (optional).
* ~~Use async operation for container management (optional)~~.
