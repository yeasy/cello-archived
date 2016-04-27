# API
These APIs will be called by front web services.

Latest API please see [api-front.yaml](api-front.yaml).

## cluster_apply

Find an available cluster in the pool for a user.

```html
GET /v1/cluster_apply
```

When `cluster_apply` request arrives, the server will try checking  available cluster in the pool.

Accordingly, the server will return a json response (succeed or fail).

## cluster_release

Declare the user will release a cluster.

```html
GET /v1/cluster_release
```

The server will drop the corresponding cluster, recreate it and put into available pool for future requests.
