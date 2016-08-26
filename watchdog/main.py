import time
import logging

from threading import Thread

from modules import host_handler, stat_handler
from common import LOG_LEVEL, log_handler

logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
logger.addHandler(log_handler)


def check_chain(period=2, retries=3):
    pass


def check_host(host, period=2, retries=3):
    for i in range(retries):
        h_freshed = host_handler.refresh_status(host.get("id"))


def watch_run(period=5):
    while True:
        logger.info("Watch dog run with period = %d s", period)
        hosts = list(host_handler.list())
        for h in hosts:
            t = Thread(target=check_host, args=(h,))
            t.start()
        time.sleep(period)


if __name__ == '__main__':
    watch_run()
