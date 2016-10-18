# API V2

Each url should have the `/v2` prefix, e.g., `/cluster_op` should be `/v2/cluster_op`.

## Rest Server
These APIs will be called by front web services.

Latest version please see [restserver.yaml](restserver.yaml).

### Operate a cluster

Basic request may looks like:

```
GET /cluster_op?action=xxx&key=value
```

or

```
POST /cluster_op
{
action:xxx,
key:value
}
```

The supported actions can be `apply`, `release`, `start`, `stop`, `restart`, etc.

We may show only one of the GET or POST request in the following sections.

#### Apply a cluster

Find an available cluster in the pool for a user.
```
GET /cluster_op?action=apply?user_id=xxxx
```

or

```
POST /cluster_op
{
action:apply,
user_id:xxx,
consensus_plugin:pbft,
consensus_mode:batch,
size:4,
allow_multiple:False
}
```

if `allow_multiple:True`, then ignore matched clusters that user already occupied.

When `apply` request arrives, the server will try checking  available cluster in the pool.

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

### release a cluster

Release a specific cluster.

```
GET /cluster_op?action=release?cluster_id=xxxx
```

or

```
POST /cluster_op
{
action:release,
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
POST /cluster_op
{
action:release,
user_id:xxxxxxxx
}
```

The server will drop the corresponding cluster, recreate it and put into available pool for future requests.


### Start, Stop or Restart a cluster

Take `start` for example.

```
GET /cluster_op?action=start&cluster_id=xxx
```

Or

```
POST /cluster_op
{
action:start,
cluster_id:xxx
}
```

### List filted clusters

Return the json object whose data may contain list of cluster ids.

Check all available cluster of given type.

```
POST /clusters
{
consensus_plugin:pbft,
consensus_mode:classic,
size:4,
user:""
}
```

Check all cluster of given type

```
POST /clusters
{
consensus_plugin:pbft,
consensus_mode:classic,
size:4,
}
```

Query the clusters for a user.

```
GET /clusters?user_id=xxx
```

or

```
POST /clusters
{
user_id:xxx
}
```

### Get object of a cluster

Return the json object whose data may contain detailed information of cluster.


```
GET /cluster/xxxxxxx
```
