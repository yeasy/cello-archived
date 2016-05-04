import datetime
import logging
import os
import sys

from threading import Thread

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
        self.collection = db["host"]

    def create(self, name, daemon_url, capacity=1, status="active"):
        """ Create a new docker host node

        :param name: name of the node
        :param daemon_url: daemon_url of the cluster
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
        if self.collection.find_one({"daemon_url": daemon_url}):
            logger.warn("{} already existed in db".format(daemon_url))
            return False


        clusters = []
        #def create_cluster_work():
        if status == "active":
            logger.debug("Init with {} clusters in host".format(capacity))
            for _ in range(capacity):
                if cluster_handler.create("{}_{}".format(name, _),
                                          daemon_url=daemon_url):
                    clusters.append("{}_{}".format(name, _))

        #if status == "active":
        #    t = Thread(target=create_cluster_work, args=())
        #    t.start()

        h = {
            'name': name,
            'daemon_url': daemon_url,
            'create_ts': datetime.datetime.now(),
            'capacity': capacity,
            'status': status,
            'clusters': clusters
        }
        ins_id = self.collection.insert_one(h).inserted_id  # object type
        self.collection.update({"_id": ins_id}, {"$set": {"id": str(ins_id)}})

        return True

    def get(self, id, serialization=False):
        """ Get a cluster

        :param id: id of the doc
        :param serialization: whether to get serialized result or object
        :return: serialized result or obj
        """
        logger.debug("Get a host with id=" + id)
        ins = self.collection.find_one({"id": id})
        if not ins:
            logger.warn("No cluster found with id=" + id)
            return {}
        if serialization:
            return self._serialize(ins)
        else:
            return ins

    def list(self, filter_data={}):
        """ List clusters with given criteria

        :param filter_data: Image with the filter properties
        :return: iteration of serialized doc
        """
        result = map(self._serialize, self.collection.find(filter_data))
        return result

    def delete(self, id):
        """ Delete a host instance

        :param id: id of the host to delete
        :return:
        """
        logger.debug("Delete a host with id={0}".format(id))

        ins = self.collection.find_one({"id": id})
        if not ins:
            logger.warn("Cannot delete non-existed host")
            return False
        # TODO: check active status
        if ins.get("clusters", ""):
            logger.warn("There are clusters on that host, cannot delete.")
            return False
        self.collection.delete_one({"id": id})
        return True

    def _serialize(self, doc, keys=['id', 'name', 'daemon_url',
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