# Database Design

We have several collections, as follows.

## cluster
Track information of active cluster.

id | api_url | name | user_id | daemon_url | create_ts| apply_ts | release_ts | node_containers
---| --------| ---- |---------| --------- | --------- | -------- | ---------- | ---------------
xxx  | http://192.168.0.1:5000| hoststr_0 | "" | tcp://192.168.0.1:2375 | 20160430101010| 20160430101010 | | [vp0,vp1,vp2,vp3]


## cluster_released
Track history of released clusters.

id | api_url | name | user_id | daemon_url | create_ts| apply_ts | release_ts | node_containers
---| --------| ---- |---------| --------- | --------- | -------- | ---------- | ---------------
xxx  | http://192.168.0.1:5000| hoststr_0 | "" | tcp://192.168.0.1:2375 | 20160430101010| 20160430101010 | 20160430101212| [vp0,vp1,vp2,vp3]
