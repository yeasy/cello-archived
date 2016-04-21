# Architecture Design

The architecture will follow those principles:

* Microservice: Means we decouple various functions to individual micro services. No service will crash others whatever it would do.
* Fault resilient: Means we do not assume any service is stable or persistent, such as the database may get disconnected any time.