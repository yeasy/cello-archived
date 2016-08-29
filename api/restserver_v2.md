# API V2

## Front
These APIs will be called by front web services.

Latest version please see [api-front.yaml](api-front.yaml).

### cluster_apply

Find an available cluster in the pool for a user.

```
POST /v2/cluster_apply
{
user_id:xxx,
consensus_plugin:pbft,
consensus_mode:batch,
size:4,
new:0
}
```

if `new:1`, then ignore matched clusters that user already occupy.

When `cluster_apply` request arrives, the server will try checking  available cluster in the pool.

Accordingly, the server will return a json response (succeed or fail).
```json
{
  "code": 200,
  "data": {
    "api_url": "http://192.168.7.62:5004",
    "consensus_mode": "batch",
    "consensus_plugin": "pbft",
    "daemon_url": "tcp://192.168.7.62:2375",
    "id": "576ba021414b0502864d0306",
    "name": "compute2_4",
    "size": 4,
    "user_id": "xxx"
  },
  "error": "",
  "status": "OK"
}
```

### cluster_release

Release a specific cluster.

```
POST /v2/cluster_release
{
cluster_id:xxxxxxxx
}
```

Return json object like
```json
{
  "code": 200,
  "data": "",
  "error": "",
  "status": "OK"
}
```

Release all clusters under a user account.

```
POST /v2/cluster_release
{
user_id:xxxxxxxx
}
```

The server will drop the corresponding cluster, recreate it and put into available pool for future requests.

### cluster_list

Return the json object whose data may contain list of cluster ids.

Check all available cluster of given type.

```
POST /v2/cluster_list
{
consensus_plugin:pbft,
consensus_mode:classic,
size:4,
user:""
}
```

Check all cluster of given type

```
POST /v2/cluster_list
{
consensus_plugin:pbft,
consensus_mode:classic,
size:4,
}
```

Query the clusters for a user.

```
POST /v2/cluster_list
{
user_id:xxx
}
```

## Admin
Those APIs should not be called by outside applications. Just for
information, please see [api-admin.yaml](api-admin.yaml)
