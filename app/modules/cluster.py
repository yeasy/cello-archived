import datetime
import logging
import os
import sys

from threading import Thread
from pymongo.collection import ReturnDocument

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from common import db, log_handler, LOG_LEVEL, get_project, col_host, \
    clean_project_containers, clean_chaincode_images, test_daemon, \
    detect_container_host, compose_start, compose_stop

from common import CLUSTER_API_PORT_START, COMPOSE_FILE_PATH, CONSENSUS_TYPES,\
    HOST_TYPES, CLUSTER_NETWORK

logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
logger.addHandler(log_handler)


class ClusterHandler(object):
    """ Main handler to operate the cluster in pool

    """
    def __init__(self):
        self.col_active = db["cluster_active"]
        self.col_released = db["cluster_released"]

    def list(self, filter_data={}, col_name="active"):
        """ List clusters with given criteria

        :param filter_data: Image with the filter properties
        :param col_name: Use data in which col_name
        :return: iteration of serialized doc
        """
        if col_name == "active":
            logger.debug("List all active clusters")
            result = map(self._serialize, self.col_active.find(filter_data))
        elif col_name == "released":
            logger.debug("List all released clusters")
            result = map(self._serialize, self.col_released.find(
                filter_data))
        else:
            logger.warn("Unknown cluster col_name=" + col_name)
            return None
        return result

    def get(self, id, serialization=False, col_name="active"):
        """ Get a cluster

        :param id: id of the doc
        :param serialization: whether to get serialized result or object
        :param col_name: collection to check
        :return: serialized result or obj
        """
        if col_name != "released":
            logger.debug("Get a cluster with id=" + id)
            ins = self.col_active.find_one({"id": id})
        else:
            logger.debug("Get a released cluster with id=" + id)
            ins = self.col_released.find_one({"id": id})
        if not ins:
            logger.warn("No cluster found with id=" + id)
            return {}
        if serialization:
            return self._serialize(ins)
        else:
            return ins

    def create(self, name, host_id, api_port=0, user_id="",
               consensus_type=CONSENSUS_TYPES[0]):
        """ Create a cluster based on given data

        TODO: maybe need other id generation mechanism

        :param name: name of the cluster
        :param host_id: id of the host URL
        :param api_port: cluster api_port, will generate if not given
        :param user_id: user_id of the cluster if start to be applied
        :param consensus_type: type of the consensus type
        :return: Id of the created cluster or None
        """
        logger.debug("Create cluster {0}, host_id={1}, consensus={2}".format(
            name, host_id, consensus_type))

        h = col_host.find_one({"id": host_id})
        if not h:
            logger.warn("Cannot find host with id="+host_id)
            return None

        if h.get("status") != "active":
            logger.warn("host {} is not active".format(host_id))
            return None

        if len(h.get("clusters")) >= int(h.get("capacity")):
            logger.warn("host {} is full already".format(host_id))
            return None

        daemon_url = h.get("daemon_url")
        logger.debug("daemon_url={}".format(daemon_url))
        if not test_daemon(daemon_url):
            logger.warn("The daemon_url is inactive or invalid:" + daemon_url)
            return None

        if api_port <= 0:
            ports = self.find_free_api_ports(host_id, 1)
            if not ports:
                logger.warn("No free port is found")
                return None
            api_port = ports[0]

        c = {
            'name': name,
            'user_id': user_id or "__NOT_READY_FOR_APPLY__",  # avoid applied
            'host_id': host_id,
            'consensus_type': consensus_type,
            'create_ts': datetime.datetime.now(),
            'release_ts': "",
            'api_url': "",
            'daemon_url': daemon_url,
        }
        cid = self.col_active.insert_one(c).inserted_id  # object type
        self.col_active.update_one({"_id": cid}, {"$set": {"id": str(cid)}})

        # start compose project
        try:
            logger.debug("Start compose project with name={}".format(str(cid)))
            containers = compose_start(name=str(cid), api_port=api_port,
                                       daemon_url=daemon_url,
                                       consensus_type=consensus_type)
        except Exception as e:
            logger.warn(e)
            logger.warn("Compose start error, then cleanup project and record")
            self.delete(id=str(cid), col_name="active", record=False,
                        forced=True)
            return None

        if not containers:
            logger.warn("containers empty, then cleanup project and record")
            self.delete(id=str(cid), col_name="active", record=False,
                        forced=True)
            return None

        # generate api url, when swarm, this must be put after compose startup
        api_url = self._gen_api_url(str(cid), h, api_port)
        if not api_url:  # not valid api_url
            logger.error("Error to gen api_url, cleanup the record and quit")
            self.col_active.delete_one({"_id": cid})
            return None

        if h:  # this part may miss some element with concurrency; dont care
            logger.debug("Add cluster to host collection")
            clusters = col_host.find_one({"id": host_id}).get("clusters")
            clusters.append(str(cid))
            col_host.update_one({"id": host_id},
                                {"$set": {"clusters": clusters}}),
        self.col_active.update_one(
            {"_id": cid},
            {"$set": {"containers": containers, "user_id": user_id,
                      'api_url': api_url}})

        logger.debug("Create cluster OK, id={}".format(str(cid)))
        return str(cid)

    def delete(self, id, col_name="active", record=False, forced=False):
        """ Delete a cluster instance, clean containers, remove db entry

        :param id: id of the cluster to delete
        :param col_name: name of the cluster to operate
        :param record: Whether to record into the released collections
        :param forced: Whether to force removing user-using cluster
        :return:
        """
        logger.debug("Delete cluster: id={}, col_name={}, forced={}".format(
            id, col_name, forced))
        if col_name == "active":
            col = self.col_active
        else:
            col = self.col_released
        if col_name == "active" and not forced:
            c = col.find_one({"id": id, "user_id": ""})  # only unused
        else:
            c = col.find_one({"id": id})
        if not c:
            logger.warn("Cannot find cluster {} in {}".format(id, col_name))
            return False
        if col_name != "active":  # released col only removes record
            col.delete_one({"id": id})
            return True
        daemon_url, api_url = c.get("daemon_url"), c.get("api_url", "")
        port = api_url.split(":")[-1] or CLUSTER_API_PORT_START
        consensus_type = c.get("consensus_type", CONSENSUS_TYPES[0])
        compose_stop(name=id, daemon_url=daemon_url, api_port=port,
                     consensus_type=consensus_type)
        clean_project_containers(daemon_url=daemon_url, name_prefix=id)
        clean_chaincode_images(daemon_url=daemon_url, name_prefix=id)
        h = col_host.find_one({"id": c.get("host_id")})
        if h:  # clean up host collection
            clusters = h.get("clusters")
            if id in clusters:
                clusters.remove(id)
            col_host.update_one({"id": c.get("host_id")},
                                {"$set": {"clusters": clusters}}),
        else:
            logger.warn("No host found for cluster="+id)
        if record:  # record to release collection
            logger.debug("Record the cluster info into released collection")
            c["release_ts"] = datetime.datetime.now()
            self.col_released.insert_one(c)
        col.delete_one({"id": id})
        return True

    def apply_cluster(self, user_id, consensus_type=CONSENSUS_TYPES[0]):
        """ Apply a cluster for a user

        :param user_id: which user will apply the cluster
        :param consensus_type: filter the cluster with consensus
        :return: serialized cluster or None
        """
        if not col_host.find_one({"status": "active"}):
            logger.warn("No active host exist for cluster applying")
            return None
        # TODO: should check already existed one first
        c = self.col_active.find_one({"user_id": user_id, "release_ts": "",
                                      "consensus_type": consensus_type})
        if not c:  # do not find assigned one, then apply new
            c = self.col_active.find_one_and_update(
                {"user_id": "", "consensus_type": consensus_type},
                {"$set": {"user_id": user_id, "apply_ts": datetime.datetime.now()}},
                return_document=ReturnDocument.AFTER)
        else:
            logger.debug("Already assigned cluster for " + user_id)
        if c and c.get("user_id") == user_id:
            logger.info("Now have cluster {} for user {}".format(c.get("id"),
                                                                 user_id))
            result = self._serialize(c, keys=['id', 'name', 'user_id',
                                              'daemon_url',
                                              'api_url', 'consensus_type'])
            h = col_host.find_one({"id": c.get("host_id")})
            return result
        else:  # Failed to find available one
            logger.warn("Not find available cluster for " + user_id)
            return None

    def release_cluster(self, user_id):
        """ Release a cluster for a user_id and recreate it.

        :param user_id: which user will apply the cluster
        :return: True or False
        """
        c = self.col_active.find_one_and_update(
            {"user_id": user_id, "release_ts": ""},
            {"$set": {"release_ts": datetime.datetime.now()}},
            return_document=ReturnDocument.AFTER)
        if not c or not c.get("release_ts"):  # not have one
            logger.warn("cluster release fail for user {}".format(user_id))
            return False

        def delete_recreate_work():
            logger.debug("Run recreate_work in background thread")
            cluster_id, cluster_name = c.get("id"), c.get("name")
            host_id, api_url = c.get("host_id"), c.get("api_url")
            if not self.delete(cluster_id, record=True, forced=True):
                logger.warn("Delete cluster error with id=" + cluster_id)
            if not self.create(name=cluster_name, host_id=host_id,
                               api_port=int(api_url.split(":")[-1])):
                logger.warn("ReCreate cluster error with name=" + cluster_name)

        t = Thread(target=delete_recreate_work, args=())
        t.start()

        return True

    def _serialize(self, doc, keys=['id', 'name', 'user_id', 'host_id',
                                    'api_url', 'consensus_type', 'daemon_url',
                                    'create_ts', 'apply_ts', 'release_ts',
                                    'containers']):
        """ Serialize an obj

        :param doc: doc to serialize
        :param keys: filter which key in the results
        :return: serialized obj
        """
        result = {}
        for k in keys:
            result[k] = doc.get(k, '')
        return result

    def _gen_api_url(self, cluster_name, host, api_port):
        """ Generate an api url automatically with given api_port

        Check existing cluster records in the host, find available one.

        :param cluster_name: name of the cluster
        :param host: Host, a single node or a swarm cluster
        :param api_port: port of the api
        :return: The generated api url address
        """
        daemon_url, host_type = host.get('daemon_url'), host.get('type')
        logger.debug("daemon_url={}, port={}".format(daemon_url,api_port))
        if api_port <= 0 or host_type not in HOST_TYPES:
            logger.warn("Invalid input: api_port=%d, host_type=%s".format(
                api_port, host_type))
            return ""
        # we should diff with simple host and swarm host here
        if host_type == HOST_TYPES[0]:  # single
            segs = daemon_url.split(":")  # tcp://x.x.x.x:2375
            if len(segs) != 3:
                logger.error("Invalid daemon url = ", daemon_url)
                return ""
            host_ip = segs[1][2:]
            logger.debug("single host, ip = {}".format(host_ip))
        elif host_type == HOST_TYPES[1]:  # swarm
            host_ip = detect_container_host(daemon_url, cluster_name+'_'+'vp0')
            logger.debug("swarm host, ip = {}".format(host_ip))
        else:
            logger.error("Unknown host type = {}".format(host_type))
            return ""
        return "http://{0}:{1}".format(host_ip, api_port)


    def find_free_api_ports(self, host_id, number):
        """ Find the first available port for a new cluster api

        This is NOT lock-free. Should keep simple, fast and safe!

        Check existing cluster records in the host, find available one.

        :param host_id: id of the host
        :param number: Number of ports to get
        :return: The port list
        """
        logger.debug("Try find {} ports for host {}".format(number, host_id))
        if number <= 0:
            logger.warn("Available number {} <= 0".format(number))
            return []
        host = col_host.find_one({"id": host_id})
        if not host:
            logger.warn("Cannot find host with id="+host_id)
            return ""

        clusters_exists = self.col_active.find({"host_id": host_id})
        ports_existed = list(map(lambda c: int(c["api_url"].split(":")[-1]),
                                 clusters_exists))

        logger.debug("The ports existed:")
        logger.debug(ports_existed)
        if len(ports_existed) + number >= 64000:
            logger.warn("Too much ports are already used.")
            return []
        candidates = [CLUSTER_API_PORT_START+i for i in range(len(
            ports_existed)+number)]
        result = [item for item in candidates if item not in ports_existed]

        logger.debug("available ports are:")
        logger.debug(result[:number])
        return result[:number]


# This will be exported as single instance for usage.
cluster_handler = ClusterHandler()