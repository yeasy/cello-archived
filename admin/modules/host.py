import datetime
import logging
import os
import sys
import time

from threading import Thread
from pymongo.collection import ReturnDocument

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from common import db, cleanup_container_host, LOG_LEVEL, setup_container_host, \
    test_daemon, detect_daemon_type, CLUSTER_API_PORT_START

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

        A docker host is potentially a single node or a swarm.
        Will full fill with clusters of given capacity.

        :param name: name of the node
        :param daemon_url: daemon_url of the host
        :param capacity: The number of clusters to hold
        :param status: active for using, inactive for not using
        :return: True or False
        """
        logger.debug("Create host: name={}, daemon_url={}, capacity={}"
                     .format(name, daemon_url, capacity))
        if not daemon_url.startswith("tcp://"):
            daemon_url = "tcp://" + daemon_url
        if not test_daemon(daemon_url):
            logger.warn("The daemon_url is inactive:" + daemon_url)
            status = "inactive"

        detected_type = detect_daemon_type(daemon_url)

        if self.col.find_one({"daemon_url": daemon_url}):
            logger.warn("{} already existed in db".format(daemon_url))
            return False

        if not setup_container_host(detected_type, daemon_url):
            logger.warn("{} cannot be setup".format(name))
            return False

        h = {
            'name': name,
            'daemon_url': daemon_url,
            'create_ts': datetime.datetime.now(),
            'capacity': capacity,
            'status': status,
            'clusters': [],
            'type': detected_type
        }
        hid = self.col.insert_one(h).inserted_id  # object type
        self.col.update_one({"_id": hid}, {"$set": {"id": str(hid)}})

        def create_cluster_work(port):
            cluster_name = "{}_{}".format(name, (port-CLUSTER_API_PORT_START))
            cid = cluster_handler.create(name=cluster_name, host_id=str(hid),
                                         api_port=port)
            if cid:
                logger.debug("Create cluster %s with id={}".format(
                    cluster_name, cid))
            else:
                logger.warn("Create cluster failed")

        if status == "active":  # active means should fillupl it
            logger.debug("Init with {} clusters in host".format(capacity))
            free_ports = cluster_handler.find_free_api_ports(str(
                hid), capacity)
            logger.debug("Free_ports = {}".format(free_ports))
            i = 0
            for p in free_ports:
                t = Thread(target=create_cluster_work, args=(p,))
                t.start()
                i += 1
                if i % 10 == 0:
                    time.sleep(0.1)

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

        TODO: may check when changing host type

        :param id: id of the host
        :param d: dict to use as updated values
        :return: serialized result or obj
        """
        logger.debug("Get a host with id=" + id)
        h_old = self._get_active_host(id)
        if not h_old:
            return {}

        daemon_url = d.get('daemon_url', h_old.get("daemon_url"))

        if "capacity" in d:
            d["capacity"] = int(d["capacity"])
        if "status" in d:
            if not test_daemon(daemon_url):
                d["status"] = 'inactive'
        h_new = self.col.find_one_and_update(
            {"id": id},
            {"$set": d},
            return_document=ReturnDocument.AFTER)

        if serialization:
            return self._serialize(h_new)
        else:
            return h_new

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

        h = self.col.find_one({"id": id})
        if not h:
            logger.warn("Cannot delete non-existed host")
            return False
        if h.get("clusters", ""):
            logger.warn("There are clusters on that host, cannot delete.")
            return False
        cleanup_container_host(h.get("daemon_url"))
        self.col.delete_one({"id": id})
        return True

    def fillup(self, id):
        """
        Fullfil a host with clusters to its capacity limit

        :param id: host id
        :return: True or False
        """
        logger.debug("fillup host with id = {}".format(id))
        host = self._get_active_host(id)
        if not host:
            return False
        num_new = host.get("capacity") - len(host.get("clusters"))
        if num_new <= 0:
            logger.warn("host already full")
            return True

        free_ports = cluster_handler.find_free_api_ports(str(id), num_new)
        logger.debug("Free_ports = {}".format(free_ports))

        def create_cluster_work(port):
            cluster_name = "{}_{}".format(host.get("name"),
                                          (port-CLUSTER_API_PORT_START))
            cid = cluster_handler.create(name=cluster_name, host_id=str(id),
                                         api_port=port)
            if cid:
                logger.debug("Create cluster %s with id={}".format(
                    cluster_name, cid))
            else:
                logger.warn("Create cluster failed")
        i = 0
        for p in free_ports:
            t = Thread(target=create_cluster_work, args=(p,))
            t.start()
            i += 1
            if i % 10 == 0:
                time.sleep(0.1)

        return True

    def clean(self, id):
        """
        Clean a host's free clusters.

        :param id: host id
        :return: True or False
        """
        logger.debug("clean host with id = {}".format(id))
        host = self._get_active_host(id)
        if not host:
            return False
        if len(host.get("clusters")) <= 0:
            return True

        host = self.col.find_one_and_update(
            {"id": id},
            {"$set": {"status": "inactive"}},
            return_document=ReturnDocument.AFTER)

        def delete_cluster_work(cid):
            cluster_handler.delete(cid),

        i = 0
        for cid in host.get("clusters"):
            t = Thread(target=delete_cluster_work, args=(cid,))
            t.start()
            i += 1
            if i % 10 == 0:
                time.sleep(0.1)

        self.col.find_one_and_update(
            {"id": id},
            {"$set": {"status": "active"}},
            return_document=ReturnDocument.AFTER)
        return True

    def _get_active_host(self, id):
        """
        Check if id exists, and status is active. Otherwise update to inactive.

        :param id: host id
        :return: host or None
        """
        logger.debug("check host with id = {}".format(id))
        host = self.col.find_one({"id": id})
        if not host:
            logger.warn("No host found with id=" + id)
            return None
        if not test_daemon(host.get("daemon_url")):
            logger.warn("Host {} is inactive".format(id))
            host = self.col.find_one_and_update(
                {"id": id},
                {"$set": {"status": "inactive"}},
                return_document=ReturnDocument.AFTER)
            return None
        return host

    def _serialize(self, doc, keys=['id', 'name', 'daemon_url', 'capacity',
                                    'type','create_ts', 'status', 'clusters']):
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