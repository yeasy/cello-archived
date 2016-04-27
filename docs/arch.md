# Architecture Design

## Philosophy and principles
The architecture will follow those principles:

* Micro-service: Means we decouple various functions to individual micro services. No service will crash others whatever it would do.
* Fault-resilience: Means we do not assume any service is stable or persistent, such as the database may get disconnected any time.
* Scalability: Try best to distribute the services, to mitigate centralized
bottle neck.

## Components

There are two main components: Master and Node.

Master node will run the poolmanager services, while docker nodes serve as
docker hosts.

Master will use remote API to start and stop hyperledger clusters in those
docker hosts.


## Implementation

The implementation is based on [Flask](flask.pocoo.org), a microframework for Python based on Werkzeug.

I choose it for:

* Lightweight
* Good enough in performance
* Flexible for extending
* Stable in code
