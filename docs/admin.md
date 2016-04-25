# Admin

Admin service is not for front users, but only for operator to take quick
look of system status or manually change configurations.

The front page is `/admin/index` to get a web page, with links to sub pages.

## Monitor

Quickly show how many active docker nodes, active block chain clusters, etc.

E.g., visit `/admin/stat` to get a web page, show basic statistic info:

* How many chain clusters are existing.
* How many users visit within a period.


## Operations

E.g., visit `/admin/operation`

* Create a cluster, with specific `daemon_url`.
* Delete a cluster, with specific uuid.
