# Cello
Blockchain as a Service Platform.

By Cello, user can 

* Request blockchains with specific configurations instantly, e.g., a 6-node chain using PBFT consensus.
* Keep a pool of numbers of running chains healthy with no human operations. 
* Check the system status, scale the chain numbers, change resources... in such a easy way.

## Features

* Smartly manage the lifecycle of blockchains, e.g., create/delete automatically.
* Nearly instant performance in service response, even with hundreds of chains.
* Support customized configuration (e.g., size, consensus) in blockchains request, currently we support [hyperledger fabric](https://github.com/hyperledger/fabric).
* Employ naive docker host or swarm host as the compute nodes.
* Deploy on top of heterogeneous architecture, e.g., z, power and x86, from bare-metal servers to virtual machines.
* Support monitor/log functionality with additional components, easy to extend.

## Docs
*It is highly recommended to carefully read these documentation first.*

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