import datetime
import logging
import os
import random
import sys
import time

from threading import Thread
from pymongo.collection import ReturnDocument

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from common import db, cleanup_container_host, LOG_LEVEL, LOG_TYPES, \
    CLUSTER_SIZES, CLUSTER_API_PORT_START, CONSENSUS_TYPES, log_handler, \
    LOGGING_LEVEL_CLUSTERS, test_daemon, detect_daemon_type, \
    reset_container_host, setup_container_host

from modules import cluster_handler

logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
logger.addHandler(log_handler)


# will be deprecated
class Host(object):
    """ Represent a host instance
    """
    def __init__(self, id='', name='', daemon_url='', capacity=1,
                 status='active', log_type=LOG_TYPES[0], log_server="",
                 log_level=LOGGING_LEVEL_CLUSTERS[0], schedulable=False):
        self.data = {
            'id': id,
            'name': name,
            'daemon_url': daemon_url,
            'create_ts': '',
            'capacity': capacity,
            'status': status,
            'clusters': [],
            'type': '',
            'log_level': log_level,
            'log_type': log_type,
            'log_server': log_server,
            'schedulable': schedulable
        }
        self.col = db["host"]

    def exist_in_db(self):
        """
        Detect whether this host is already in db.

        :return: True for existence, otherwise False
        """
        if self.col.find_one(self.get_data('daemon_url')):
            logger.warn("{} already in db".format(self.get('daemon_url')))
            return True
        else:
            return False

    def insert_to_db(self):
        """
        Insert this host to the db.
        This should be only called once for each host

        :return: host data or None
        """
        if self.exist_in_db():
            return None
        hid = self.col.insert_one(self.data).inserted_id  # object type
        create_ts = datetime.datetime.now()
        host = self.col.find_one_and_update(
            {"_id": hid},
            {"$set": {
                "id": str(hid),
                'create_ts': create_ts
            }
            },
            return_document=ReturnDocument.AFTER)
        self.set(id=str(hid), create_ts=create_ts)
        return self.get_data()

    def set(self, sync=False, **kwargs):
        """
        Set the key:value pairs to the data
        :param sync: Whether to sync to db
        :param kwargs: kv pairs
        :return: True of False
        """
        self.data.update(kwargs)
        if sync:
            host = self.col.find_one_and_update(
                {"id": self.get('id')},
                {"$set": kwargs},
                return_document=ReturnDocument.AFTER)
            if not host:
                return False
        return True

    def get(self, key):
        """
        Get the specific key's value in data.

        :param key:
        :return:
        """
        return self.data.get(key)

    def get_data(self, *keys):
        """
        Get the data as a dict

        :param keys: filter which key in the results
        :return: dict obj
        """
        if not keys:
            return self.data
        else:
            result = {}
            for k in keys:
                if k in self.data:
                    result[k] = self.data[k]
            return result


class HostHandler(object):
    """ Main handler to operate the Docker hosts
    """
    def __init__(self):
        self.col = db["host"]

    def create(self, name, daemon_url, capacity=1,
               log_level=LOGGING_LEVEL_CLUSTERS[0],
               log_type=LOG_TYPES[0], log_server="", fillup=False,
               schedulable=False, serialization=True):
        """ Create a new docker host node

        A docker host is potentially a single node or a swarm.
        Will full fill with clusters of given capacity.

        :param name: name of the node
        :param daemon_url: daemon_url of the host
        :param capacity: The number of clusters to hold
        :param log_type: type of the log
        :param log_level: level of the log
        :param log_server: server addr of the syslog
        :param fillup: Whether fillup after creation
        :param schedulable: Whether can schedule cluster request to it
        :param serialization: whether to get serialized result or object
        :return: True or False
        """
        logger.debug("Create host: name={}, daemon_url={}, capacity={}, "
                     "log={}/{}, fillup={}, schedulable={}"
                     .format(name, daemon_url, capacity, log_type,
                             log_server, fillup, schedulable))
        if not daemon_url.startswith("tcp://"):
            daemon_url = "tcp://" + daemon_url

        if self.col.find_one({"daemon_url": daemon_url}):
            logger.warn("{} already existed in db".format(daemon_url))
            return {}

        if "://" not in log_server:
            log_server = "udp://" + log_server
        if log_type == LOG_TYPES[0]:
            log_server = ""
        if test_daemon(daemon_url):
            logger.warn("The daemon_url is active:" + daemon_url)
            status = "active"
        else:
            logger.warn("The daemon_url is inactive:" + daemon_url)
            status = "inactive"

        detected_type = detect_daemon_type(daemon_url)

        if not setup_container_host(detected_type, daemon_url):
            logger.warn("{} cannot be setup".format(name))
            return {}

        h = {
            'name': name,
            'daemon_url': daemon_url,
            'create_ts': datetime.datetime.now(),
            'capacity': capacity,
            'status': status,
            'clusters': [],
            'type': detected_type,
            'log_level': log_level,
            'log_type': log_type,
            'log_server': log_server,
            'schedulable': schedulable
        }
        hid = self.col.insert_one(h).inserted_id  # object type
        host = self.col.find_one_and_update(
            {"_id": hid},
            {"$set": {"id": str(hid)}},
            return_document=ReturnDocument.AFTER)

        if capacity > 0 and fillup:  # should fillup it
            self.fillup(str(hid))

        if serialization:
            return self._serialize(host)
        else:
            return host

    def get(self, id):
        """ Get a host

        :param id: id of the doc
        :return: serialized result or obj
        """
        logger.debug("Get a host with id=" + id)
        ins = self.col.find_one({"id": id})
        if not ins:
            logger.warn("No cluster found with id=" + id)
            return {}
        return self._serialize(ins)

    def update(self, id, d):
        """ Update a host

        TODO: may check when changing host type

        :param id: id of the host
        :param d: dict to use as updated values
        :return: serialized result or obj
        """
        logger.debug("Get a host with id=" + id)
        h_old = self.col.find_one({"id": id})
        if not h_old:
            logger.warn("No host found with id=" + id)
            return {}

        if "daemon_url" in d and not d["daemon_url"].startswith("tcp://"):
            d["daemon_url"] = "tcp://" + d["daemon_url"]

        if "capacity" in d:
            d["capacity"] = int(d["capacity"])
        if d["capacity"] < len(h_old.get("clusters")):
            logger.warn("Cannot set cap smaller than running clusters")
            return {}
        if "log_server" in d and "://" not in d["log_server"]:
            d["log_server"] = "udp://" + d["log_server"]
        if "log_type" in d and d["log_type"] == LOG_TYPES[0]:
            d["log_server"] = ""
        h_new = self.update_to_db(id, d)
        return self._serialize(h_new)

    def list(self, filter_data={}, validate=False):
        """ List hosts with given criteria

        :param filter_data: Image with the filter properties
        :param validate: validate the host status before list
        :return: iteration of serialized doc
        """
        host_docs = self.col.find(filter_data)

        def update_work(host):
            self.refresh_status(host.get("id"))
        if validate:
            logger.debug("update host status")
            for h in host_docs:
                t = Thread(target=update_work, args=(h,))
                t.start()
        hosts = self.col.find(filter_data)
        result = map(self._serialize, hosts)
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
            logger.warn("host fillup failed as inactive status")
            return False
        num_new = host.get("capacity") - len(host.get("clusters"))
        if num_new <= 0:
            logger.warn("host already full")
            return True

        free_ports = cluster_handler.find_free_api_ports(id, num_new)
        logger.debug("Free_ports = {}".format(free_ports))

        def create_cluster_work(port):
            cluster_name = "{}_{}".format(host.get("name"),
                                          (port - CLUSTER_API_PORT_START))
            consensus_plugin, consensus_mode = random.choice(CONSENSUS_TYPES)
            cluster_size = random.choice(CLUSTER_SIZES)
            cid = cluster_handler.create(name=cluster_name, host_id=id,
                                         api_port=port,
                                         consensus_plugin=consensus_plugin,
                                         consensus_mode=consensus_mode,
                                         size=cluster_size)
            if cid:
                logger.debug("Create cluster %s with id={}".format(
                    cluster_name, cid))
            else:
                logger.warn("Create cluster failed")
        for p in free_ports:
            t = Thread(target=create_cluster_work, args=(p,))
            t.start()
            time.sleep(1.0)

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

        host = self.update_to_db(id, schedulable=False)

        for cid in host.get("clusters"):
            t = Thread(target=cluster_handler.delete, args=(cid,))
            t.start()
            time.sleep(0.2)
        self.update_to_db(id, schedulable=True)

        return True

    def reset(self, id):
        """
        Clean a host's free clusters.

        :param id: host id
        :return: True or False
        """
        logger.debug("clean host with id = {}".format(id))
        host = self._get_active_host(id)
        if not host or len(host.get("clusters")) > 0:
            logger.warn("no resettable host is found with id ={}".format(id))
            return False
        return reset_container_host(host_type=host.get("type"),
                                    daemon_url=host.get("daemon_url"))

    def refresh_status(self, id):
        """
        Refresh the status of the host by detection

        :param host: the host to update status
        :return: Updated host
        """
        host = self.col.find_one({"id": id, "status": "active"})
        if not host:
            logger.warn("No host found with id=" + id)
            return None
        if not test_daemon(host.get("daemon_url")):
            logger.warn("Host {} is inactive".format(id))
            return self.update_to_db(id, status="inactive")
        else:
            return self.update_to_db(id, status="active")

    def is_active(self, host):
        """
        Update status of the host

        :param host: the host to update status
        :return: Updated host
        """
        if not host:
            logger.warn("invalid host is given")
            return False
        return host.get("status") == "active"

    def _get_active_host(self, id):
        """
        Check if id exists, and status is active. Otherwise update to inactive.

        :param id: host id
        :return: host or None
        """
        logger.debug("check host with id = {}".format(id))
        host = self.col.find_one({"id": id, "status": "active"})
        if not host:
            logger.warn("No host found with id=" + id)
            return None
        return self._serialize(host)

    def _serialize(self, doc, keys=['id', 'name', 'daemon_url', 'capacity',
                                    'type', 'create_ts', 'status',
                                    'schedulable', 'clusters', 'log_level',
                                    'log_type', 'log_server']):
        """ Serialize an obj

        :param doc: doc to serialize
        :param keys: filter which key in the results
        :return: serialized obj
        """
        result = {}
        for k in keys:
            result[k] = doc.get(k, '')
        return result

    def update_to_db(self, id, **kwargs):
        """
        Set the key:value pairs to the data
        :param id: Which host to update
        :param kwargs: kv pairs
        :return: The updated host
        """
        host = self.col.find_one_and_update(
            {"id": id},
            {"$set": kwargs},
            return_document=ReturnDocument.AFTER)
        return host


host_handler = HostHandler()
