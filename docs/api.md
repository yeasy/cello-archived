# API

## find_available

Find an available chain in the pool.

```html
GET /apply_cluster
```

When `apply_cluster` request arrives, the server will check `available_cluster` table to get a cluster instance or null.

Accordingly, the server will return a json response like

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
    "error": "something goes wrong"
    "metadata":{
        "req_id":"abcdefg"
    }
}
```

## stop

Stop a chain.

## start

Start a chain.

