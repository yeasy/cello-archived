# User Scenarios

## apply a cluster

User sends request to apply a cluster, pm will check the db, to find if there's one with user_id empty (means available for apply).

If found one, construct the response, otherwise, contruct an error response.


## release a cluster

User sends request to release a cluster, pm will check the `user_id` in the
request, to see if there is one in the db.

If found, then release and recreate it with the same name, using the same
`daemon_url` through compose API, and move it to released db collections.

If not found, then just ignore or send some error msg in response.
