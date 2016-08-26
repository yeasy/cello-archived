# Architecture Design

## Philosophy and principles
The architecture will follow those principles:

* Micro-service: Means we decouple various functions to individual micro services. No service will crash others whatever it would do.
* Fault-resilience: Means we do not assume any service is stable or persistent, such as the database may get disconnected any time.
* Scalability: Try best to distribute the services, to mitigate centralized bottle neck.

## Node Types

There are two kinds of nodes: Master and Compute.

Master node will run the poolmanager services, while compute nodes serve as container hosts.

Master will use remote API to start and stop hyperledger clusters in those compute nodes.

## Components

* `admin`: Provide the dashboard for the pool administrator, also the core
engine to maintain everything.
* `app`: Provide the restful api for other system to apply/release/list chains.
* `watchdog`: periodly checking system status, keep everything healthy and
clean.

## Implementation

The implementation is based on [Flask](flask.pocoo.org), a microframework for Python based on Werkzeug.

I choose it for:

* Lightweight
* Good enough in performance
* Flexible for extending
* Stable in code
