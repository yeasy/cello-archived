# Dashboard

Dashboard service is not for front users, but only for operator to take quick
look of system status or manually change configurations.

The front page is `/admin` to get a web page, with links to sub pages.

## clusters

Visit `/clusters`.

* Create a cluster, with specific `daemon_url`.
* Delete a cluster, with specific uuid.

## clusters_released

Visit `/clusters_released`.

History data of the released clusters.

## Monitor

TODO.

Quickly show how many active docker nodes, active block chain clusters, etc.

E.g., visit `/admin/stat` to get a web page, show basic statistic info:

* How many chain clusters are existing.
* How many users visit within a period.

## Screenshots

![dashboard-main](imgs/dashboard_main.png)
![dashboard-status](imgs/dashboard_status.png)
![dashboard-hosts](imgs/dashboard_hosts.png)
![dashboard-clusters](imgs/dashboard_clusters.png)
![dashboard-add-host](imgs/dashboard_add_host.png)
![dashboard-add-cluster](imgs/dashboard_add_cluster.png)
