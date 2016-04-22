# API

## External APIs
### apply_cluster

Find an available cluster in the pool.

```html
GET /apply_cluster
```

When `apply_cluster` request arrives, the server will check  available
cluster in the pool.

Accordingly, the server will return a json response (succeed or fail).

* When succeed:

```json
{
    "status": "OK",
    "cluster": {
        "id": "xxxxx",
        "api_url": "192.168.0.2:5000"
    },
    "error": "",
    "metadata":{
        "req_id":"abcdefg"
    }
}
```

* When error:

```json
{
    "status": "ERROR",
    "error": "something goes wrong",
    "metadata":{
        "req_id":"abcdefg"
    }
}
```

## stop

Stop a chain.

## start

Start a chain.

