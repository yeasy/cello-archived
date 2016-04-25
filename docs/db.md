# Database Design

We have several tables, as follows.

## cluster_active
Track information of active cluster.

id | api_url | name | user_id | daemon_url | apply_ts | drop_ts
---- | --------| ------------ |---------| --------- | --------- |-------
xxx  | http://192.168.0.1:5000| hoststr_0 | "" | tcp://192.168.0.1:2375 | 20160430101010 |


## cluster_dropped
Track history of dropped clusters.

id | api_url | project_name | user_id | daemon_url | apply_ts | drop_ts
---- | --------| ------------ |---------| --------- | --------- |-------
xxx  | http://192.168.0.1:5000| hoststr_0 | "xiaoming" | tcp://192.168.0.1:2375 | 20160430101010 | 20160430121212

