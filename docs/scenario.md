# User Scenarios

## apply a cluster

User sends request to apply a cluster, pm will check the `cluster_active`
table, to find if there's one with user_id empty (means available for apply).

If found one, construct the response, otherwise, contruct an error response.


## drop a cluster

User sends request to drop a cluster, pm will check the `user_id` in the
request, to see if there is one in the `cluster_active` table.

If found, then drop and recreate it with same `project_name` using the same
`daemon_url` through compose API, and move it to the `cluster_dropped` table.

If not found, then just ignore or send some error msg in response.

