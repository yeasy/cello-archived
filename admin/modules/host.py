import datetime
import logging
import os
import sys
import time

from threading import Thread
from pymongo.collection import ReturnDocument

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from common import db, log_handler, LOG_LEVEL, get_project, \
    clean_exited_containers, clean_chaincode_images, check_daemon_url, \
    CLUSTER_API_PORT_START, COMPOSE_FILE_PATH

from modules import cluster_handler

logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)

class HostHandler(object):
    """ Main handler to operate the Docker hosts

    """
    def __init__(self):
        self.col = db["host"]

    def create(self, name, daemon_url, capacity=1, status="active"):
        """ Create a new docker host node

        :param name: name of the node
        :param daemon_url: daemon_url of the host
        :param capacity: The number of clusters to hold
        :param status: active for using, inactive for not using
        :return: True or False
        """
        logger.debug("Create new host with name={0}, daemon_url={1}, "
                     "capacity={2}".format(name, daemon_url, capacity))
        if not daemon_url.startswith("tcp://"):
            daemon_url = "tcp://" + daemon_url
        if not check_daemon_url(daemon_url):
            logger.warn("The daemon_url is inactive:" + daemon_url)
            status = "inactive"
        if self.col.find_one({"daemon_url": daemon_url}):
            logger.warn("{} already existed in db".format(daemon_url))
            return False

        h = {
            'name': name,
            'daemon_url': daemon_url,
            'create_ts': datetime.datetime.now(),
            'capacity': capacity,
            'status': status,
            'clusters': []
        }
        hid = self.col.insert_one(h).inserted_id  # object type
        self.col.update_one({"_id": hid}, {"$set": {"id": str(hid)}})

        def create_cluster_work():
            logger.debug("Init with {} clusters in host".format(capacity))
            for _ in range(capacity):
                cid = cluster_handler.create("{}_{}".format(name, _), str(hid))
                logger.debug("Create cluster with id={}".format(cid))
                time.sleep(1)

        if status == "active":
            t = Thread(target=create_cluster_work, args=())
            t.start()

        return True

    def get(self, id, serialization=False):
        """ Get a host

        :param id: id of the doc
        :param serialization: whether to get serialized result or object
        :return: serialized result or obj
        """
        logger.debug("Get a host with id=" + id)
        ins = self.col.find_one({"id": id})
        if not ins:
            logger.warn("No cluster found with id=" + id)
            return {}
        if serialization:
            return self._serialize(ins)
        else:
            return ins

    def update(self, id, d, serialization=True):
        """ Update a host

        :param id: id of the host
        :param d: dict to use as updated values
        :return: serialized result or obj
        """
        logger.debug("Get a host with id=" + id)

        ins = self.col.find_one_and_update(
            {"id": id},
            {"$set": d},
            return_document=ReturnDocument.AFTER)

        if not ins:
            logger.warn("No Host found with id=" + id)
            return {}
        if serialization:
            return self._serialize(ins)
        else:
            return ins

    def list(self, filter_data={}):
        """ List hosts with given criteria

        :param filter_data: Image with the filter properties
        :return: iteration of serialized doc
        """
        result = map(self._serialize, self.col.find(filter_data))
        return result

    def delete(self, id):
        """ Delete a host instance

        :param id: id of the host to delete
        :return:
        """
        logger.debug("Delete a host with id={0}".format(id))

        ins = self.col.find_one({"id": id})
        if not ins:
            logger.warn("Cannot delete non-existed host")
            return False
        if ins.get("clusters", ""):
            logger.warn("There are clusters on that host, cannot delete.")
            return False
        self.col.delete_one({"id": id})
        return True

    def _serialize(self, doc, keys=['id', 'name', 'daemon_url', 'capacity',
                                    'create_ts', 'status', 'clusters']):
        """ Serialize an obj

        :param doc: doc to serialize
        :param keys: filter which key in the results
        :return: serialized obj
        """
        result = {}
        for k in keys:
            result[k] = doc.get(k, '')
        return result

host_handler = HostHandler()