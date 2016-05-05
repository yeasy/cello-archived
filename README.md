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

*TODO: We may need a setup script.*

All services are setup through Docker containers by default.

### Master Requirement
* docker engine: >=1.10.0
* docker-compose: >=1.7.0
* docker images:
    - python:3.5
    - mongo:3.2
    - yeasy/nginx

### Node Requirement

* docker engine:
    - >=1.10.0,
    - let daemon listen on port 2375, and make sure Master can reach Node from port 2375.
```sh
# Add this into /etc/default/docker
DOCKER_OPTS="$DOCKER_OPTS -H tcp://0.0.0.0:2375 -H unix:///var/run/docker.sock"
```
* docker images:
    - yeasy/hyperledger (After pulling, rename to openblockchain/baseimage)
    - yeasy/hyperledger-peer (match with the [compose](admin/common/compose-defaults.yml) file)
    - yeasy/hyperledger-membersrvc (optional, only when need the authentication service)
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

### Start
After all required images and tools are prepared in all nodes, you can start
the poolmanager service by running

```sh
$ bash ./scripts/start.sh
```

## Dependency

* [app requirements](app/requirements.txt)
* [admin requirements](admin/requirements.txt)


## TODO
* ~~Add default 404 and 500 error page.~~
* ~~Add doc for all methods and classes~~.
* Admin: Add authentication for user login.
* Admin: Update api definitions in yml files (optional).
* ~~Admin: Add host module to add cluster in batch (optional).~~
* ~~Use async operation for container management (optional)~~.
* Support multiple version in API.
* ~~Support pagination~~.
* ~~Support updating the host config~~.
* Support user defined cluster configuration.
* ~~Add form validation~~.
