import time
import logging

from threading import Thread

from modules import host_handler, cluster_handler
from common import LOG_LEVEL, log_handler

logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
logger.addHandler(log_handler)


def chain_check_health(chain_id, period=2, retries=3):
    pass


def host_check_chains(host_id):
    clusters = cluster_handler.list(filter_data={"host_id": host_id})
    for c in cluster:
        t = Thread(target=chain_check_health, args=(c.get("id"),))
        t.start()
    pass


def host_check(host_id, period=2, retries=3):
    for i in range(retries):
        h_freshed = host_handler.refresh_status(host_id)
        if host_handler.is_active(host_id):  # host is active
            logger.debug("host {} is active, check its chain", host_id)
            host_check_chains(host_id)


def watch_run(period=5):
    """
    Run the checking in period.

    :param period: Wait period between two checking
    :return:
    """
    while True:
        logger.info("Watch dog run with period = %d s", period)
        hosts = list(host_handler.list())
        for h in hosts:
            t = Thread(target=host_check, args=(h.get("id"),))
            t.start()
        time.sleep(period)


if __name__ == '__main__':
    watch_run()
