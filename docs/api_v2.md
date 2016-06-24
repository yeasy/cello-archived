# API

## Front
These APIs will be called by front web services.

Latest version please see [api-front.yaml](api-front.yaml).

### cluster_apply
This keeps the same option with `v2`.

Find an available cluster in the pool for a user.

```
GET /v2/cluster_apply?user_id=xxx&consensus_plugin=pbft&consensus_mode
=classic&size=4&new=0
```

if add `new=1`, then ignore matched clusters that user already occupy.

When `cluster_apply` request arrives, the server will try checking  available cluster in the pool.

Accordingly, the server will return a json response (succeed or fail).

### cluster_release
This keeps the same option with `v2`.

Release a specific cluster.

```
GET /v2/cluster_release?cluster_id=xxxxxxxx
```

Release all clusters under a user account.
```
GET /v2/cluster_release?user_id=xxxxxxxx
```
The server will drop the corresponding cluster, recreate it and put into available pool for future requests.

### cluster_list

Return the json object whose data may contain list of cluster ids.

Check the available cluster of given type.

```
GET /v2/cluster_list?consensus_plugin=pbft&consensus_mode=classic
&size=4&used=0
```

Check all cluster of given type

```
GET /v2/cluster_list?consensus_plugin=pbft&consensus_mode=classic
&size=4
```

Query the clusters for a user.

```
GET /v2/cluster_list?user_id=xxx
```

## Admin
Those APIs should not be called by outside applications. Just for
information, please see [api-admin.yaml](api-admin.yaml)
