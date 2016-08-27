# Cello
Platform to support Blockchain as a Service.

## Features

* Smartly manage ledger clusters, e.g., create/delete host,
* Provide REST API for user and dashboard for operators.
* Support most kind of IaaS, including bare-metal or virtual machine.
* Provide dedicated cluster to user instantly after request arrives.
* User can select what kind of cluster he want.
* Support naive docker host or swarm cluster API.
* Automatically maintain clusters resources in pool when error happens.
* Support monitor functionality with additional components.

## Docs
*It is highly recommended to carefully read these documentation before
taking any other action.*

* [Terminology](docs/terminology.md)
* [Deployment](docs/deployment.md)
* [Scenarios](docs/scenario.md)
* [API](docs/api_v2.md)
* [Architecture Design](docs/arch.md)
* [Database Model](docs/db.md)
* [engine](docs/admin.md)

## TODO
* ~~Add default 404 and 500 error page.~~
* ~~Add doc for all methods and classes~~.
* ~~engine: Add authentication for user login~~.
* ~~engine: Add host module to add cluster in batch (optional).~~
* ~~Use async operation for container management (optional).~~
* ~~Support multiple version in API.~~
* ~~Support pagination~~.
* ~~Support updating the host config~~.
* ~~Support user defined cluster configuration.~~
* ~~Add form validation~~.
* ~~Support metadata field from user apply cluster.~~
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
* engine: Update api definitions yml files (optional).
* Support auto fresh based on websocket.
* Refine setup scripts.

## Author
Designed and maintained by [Baohua Yang](yangbaohua@gmail.com).

## Why names Cello?
Can u find anyone better at playing chains?