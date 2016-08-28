import time
import logging

from threading import Thread

from modules import host_handler, cluster_handler
from common import LOG_LEVEL, log_handler

logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
logger.addHandler(log_handler)


def chain_check_health(chain_id, retries=3):
    """
    Check the chain health.

    :param chain_id:
    :param retries:
    :return:
    """
    #if not cluster_handler.check_health(chain_id) \
    #        and c['user_id'] != SYS_UNHEALTHY:
    #    cluster_handler.release_cluster(c['id'], record=False)
    pass


def host_check_chains(host_id):
    """
    Check one host.

    :param host_id:
    :return:
    """
    clusters = cluster_handler.list(filter_data={"host_id": host_id})
    for c in clusters:
        t = Thread(target=chain_check_health, args=(c.get("id"),))
        t.start()
        t.join(timeout=5)


def host_check(host_id, period=2, retries=3):
    """
    Run check on specific host.
    Check status and check each chain's health.

    :param host_id: id of the checked host
    :param period: retry wait
    :param retries: how many retries before thnking it's inactive
    :return:
    """
    for i in range(retries):
        h_freshed = host_handler.refresh_status(host_id)
        if h_freshed.get_by_id("status") == "active":  # host is active
            logger.debug("host {} is active, check its chain".format(host_id))
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
            t.join(timeout=30)
        time.sleep(period)


if __name__ == '__main__':
    watch_run()
