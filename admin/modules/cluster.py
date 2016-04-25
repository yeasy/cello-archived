import __future__

import datetime
import logging
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from common import get_project, db, log_handler

from common.utils import CLUSTER_API_PORT_START

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(log_handler)


class Cluster(object):
    def __init__(self):
        self.id = ""
        self.name = ""
        self.api_url = ""
        self.user_id = ""
        self.daemon_url = ""
        self.apply_ts = ""
        self.drop_ts = ""

    def get(self):
        return self._serialize()

    def create(self, name, daemon_url):
        self.apply_ts = datetime.datetime.utcnow()
        pass

    def delete(self):
        pass

    def _serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'user_id': self.user_id,
            'api_url': self.api_url,
            'daemon_url': self.daemon_url,
            'apply_ts': self.apply_ts,
            'drop_ts': self.drop_ts,
        }


class ClusterHandler(object):
    def __init__(self):
        self.collections = db["cluster"]

    def _gen_api_url(self, daemon_url):
        """ Generate an api url automatically.
        :param daemon_url, may look like: tcp://192.168.0.1:2375
        :param d
        """
        logger.info("gen_api_url")
        segs = daemon_url.split(":")
        if len(segs) != 3:
            logger.error("invalid daemon url = ", daemon_url)
            return None
        host_ip = segs[1][2:]
        exists = self.collections.find({"daemon_url": daemon_url})
        api_url_existed = map(lambda c: c["api_url"], exists)
        logger.info("existing api_urls", api_url_existed)
        for i in range(len(api_url_existed)):
            new_url = "http://{0}:{1}".format(host_ip, CLUSTER_API_PORT_START
                                            + i)
            if new_url not in api_url_existed:
                return new_url
        logger.warn("no valid api_url is generated")
        return None

    def list(self):
        logger.info("list all clusters")
        result = map(self._serialize, self.collections.find())
        return result

    def get(self, id):
        logger.info("get a cluster")
        return self.collections.find_one({"id": id})

    def create(self, name, daemon_url, api_url="", user_id=""):
        """ create a cluster
        TODO: maybe need other id generation mechanism

        :return json obj
        """
        logger.info("create a cluster")
        if not api_url:  # automatically schedule one
            api_url = self._gen_api_url(daemon_url)
        c = {
                'name': name,
                'user_id': user_id,
                'api_url': api_url,
                'daemon_url': daemon_url,
                'apply_ts': datetime.datetime.utcnow(),
                'drop_ts': "",
            }
        ins_id = self.collections.insert_one(c).inserted_id
        c['id'] = ins_id.toString()
        return c

    @classmethod
    def delete(self, id):
        logger.info("delete a cluster")
        self.collections.delete_one({"id": id})

    def _serialize(self, c):
        return {
            'id': c.id,
            'name': c.name,
            'user_id': c.user_id,
            'api_url': c.api_url,
            'daemon_url': c.daemon_url,
            'apply_ts': c.apply_ts,
            'drop_ts': c.drop_ts,
        }

cluster_handler = ClusterHandler()