import os
import logging

log_handler = logging.StreamHandler()

# noqa
# [2016-04-28 01:51:06,044] INFO [resources.cluster] [cluster.py:20 clusters_show()] - /clusters action_v1=GET
formatter = logging.Formatter("[%(asctime)s] %(levelname)s [%(name)s]"
                              " [%(filename)s:%(lineno)s %(funcName)20s()]"
                              " - %(message)s")
log_handler.setFormatter(formatter)

LOG_LEVEL = eval("logging."+os.environ.get("LOG_LEVEL", "INFO"))
