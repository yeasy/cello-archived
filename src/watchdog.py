import time
import logging

from threading import Thread

from modules import host_handler, cluster_handler
from common import LOG_LEVEL, log_handler, SYS_DELETER, SYS_USER

logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
logger.addHandler(log_handler)


def chain_check_health(chain_id, retries=3, period=2):
    """
    Check the chain health.

    :param chain_id: id of the chain
    :param retries: how many retries before thinking not health
    :param period: wait between two retries
    :return:
    """
    # if not cluster_handler.check_health(chain_id) \
    #        and c['user_id'] != SYS_UNHEALTHY:
    #    cluster_handler.release_cluster(c['id'], record=False)
    logger.debug("Chain {}: checking health".format(chain_id))
    chain = cluster_handler.get_by_id(chain_id)
    if not chain:
        logger.warn("Not find chain with id = {}".format(chain_id))
        return
    chain_user_id = chain.get("user_id")
    if chain_user_id.startswith(SYS_USER):  # in system processing
        for i in range(retries):
            if cluster_handler.get_by_id(chain_id).get("user_id") != \
                    chain_user_id or \
                    cluster_handler.refresh_health(chain_id):
                return
            else:
                time.sleep(period)
        if cluster_handler.get_by_id(chain_id).get("user_id") == chain_user_id:
            logger.info("Deleting frozen-in-process chain {}".format(chain_id))
            cluster_handler.delete(chain_id)
        return
    # free or used by user
    for i in range(retries):
        if cluster_handler.refresh_health(chain_id):  # chain is healthy
            return
        else:
            time.sleep(period)
    logger.debug("Chain {} is unhealthy!".format(chain_id))
    if cluster_handler.get_by_id(chain_id).get("user_id") == "":
        logger.info("Resetting free unhealthy chain {}".format(chain_id))
        cluster_handler.reset_free_one(chain_id)


def host_check_chains(host_id):
    """
    Check one host.

    :param host_id:
    :return:
    """
    logger.debug("Host {}: checking cluster health".format(host_id))
    clusters = cluster_handler.list(filter_data={"host_id": host_id})
    for c in clusters:
        t = Thread(target=chain_check_health, args=(c.get("id"),))
        t.start()
        t.join(timeout=5)


def host_check(host_id, retries=3, period=2):
    """
    Run check on specific host.
    Check status and check each chain's health.

    :param host_id: id of the checked host
    :param retries: how many retries before thnking it's inactive
    :param period: retry wait
    :return:
    """
    for _ in range(retries):
        if host_handler.refresh_status(host_id):  # host is active
            logger.debug("host {} is active, check its chains".format(host_id))
            host_check_chains(host_id)
            break
        time.sleep(period)


def watch_run(period=15):
    """
    Run the checking in period.

    :param period: Wait period between two checking
    :return:
    """
    while True:
        logger.info("Watchdog run checks with period = %d s", period)
        hosts = list(host_handler.list())
        for h in hosts:
            t = Thread(target=host_check, args=(h.get("id"),))
            t.start()
            t.join(timeout=period)
        time.sleep(period)


if __name__ == '__main__':
    watch_run()
