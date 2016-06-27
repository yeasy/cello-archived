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

from common import CLUSTER_API_PORT_START, CONSENSUS_PLUGINS, \
    CONSENSUS_MODES, HOST_TYPES, SYS_CREATOR, SYS_DELETER, CLUSTER_SIZES

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
            return []
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
               consensus_plugin=CONSENSUS_PLUGINS[0],
               consensus_mode=CONSENSUS_MODES[0], size=CLUSTER_SIZES[0]):
        """ Create a cluster based on given data

        TODO: maybe need other id generation mechanism

        :param name: name of the cluster
        :param host_id: id of the host URL
        :param api_port: cluster api_port, will generate if not given
        :param user_id: user_id of the cluster if start to be applied
        :param consensus_plugin: type of the consensus type
        :param size: size of the cluster, int type
        :return: Id of the created cluster or None
        """
        logger.info("Create cluster {}, host_id={}, consensus={}/{}, "
                    "size={}".format(
            name, host_id, consensus_plugin, consensus_mode, size))

        h = self._get_active_host(host_id)
        if not h:
            return None

        if len(h.get("clusters")) >= h.get("capacity"):
            logger.warn("host {} is full already".format(host_id))
            return None

        daemon_url = h.get("daemon_url")
        logger.debug("daemon_url={}".format(daemon_url))

        if api_port <= 0:
            ports = self.find_free_api_ports(host_id, 1)
            if not ports:
                logger.warn("No free port is found")
                return None
            api_port = ports[0]

        c = {
            'name': name,
            'user_id': user_id or SYS_CREATOR,  # avoid applied
            'host_id': host_id,
            'consensus_plugin': consensus_plugin,
            'consensus_mode': consensus_mode,
            'create_ts': datetime.datetime.now(),
            'release_ts': "",
            'duration': "",
            'api_url': "",  # This will be generate later
            'daemon_url': daemon_url,
            'size': size,
            'containers': [],
        }
        cid = self.col_active.insert_one(c).inserted_id  # object type
        self.col_active.update_one({"_id": cid}, {"$set": {"id": str(cid)}})
        # try to add one cluster to host
        h = col_host.find_one_and_update({"id": host_id},
                                         {"$addToSet": {"clusters": str(cid)}},
                                         return_document=ReturnDocument.AFTER)
        if not h or len(h.get("clusters")) > h.get("capacity"):
            self.col_active.delete_one({"_id": cid})
            col_host.update_one({"id": host_id},
                                {"$pull": {"clusters": str(cid)}}),
            return None

        # from now on, we should be safe

        # start compose project, failed then clean and return
        try:
            logger.debug("Start compose project with name={}".format(str(cid)))
            containers = compose_start(name=str(cid), api_port=api_port,
                                       host=h,
                                       consensus_plugin=consensus_plugin,
                                       consensus_mode=consensus_mode,
                                       cluster_size=size)
        except Exception as e:
            logger.warn(e)
            logger.warn("Compose start error, then delete project and record")
            self.delete(id=str(cid), col_name="active", record=False,
                        forced=True)
            return None
        if not containers or int(size) != len(containers):
            logger.warn("failed containers={}, then delete cluster".format(
                len(containers)))
            self.delete(id=str(cid), col_name="active", record=False,
                        forced=True)
            return None

        # no api_url, then clean and return
        api_url = self._gen_api_url(str(cid), h, api_port)
        if not api_url:  # not valid api_url
            logger.error("Error to gen api_url, cleanup the record and quit")
            self.delete(id=str(cid), col_name="active", record=False,
                        forced=True)
            return None

        # update api_url, container, and user_id field
        self.col_active.update_one(
            {"_id": cid},
            {"$set": {"containers": containers, "user_id": user_id,
                      'api_url': api_url}})

        logger.info("Create cluster OK, id={}".format(str(cid)))
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

        if col_name != "active":  # released col only removes record
            self.col_released.find_one_and_delete({"id": id})
            return True
        c = self.col_active.find_one_and_update(
            {"id": id},
            {"$set": {"user_id": SYS_DELETER}},
            return_document=ReturnDocument.BEFORE)  # db has new user_id
        if not c:
            logger.warn("Cannot find cluster {} in {}".format(id, col_name))
            return False
        # we are safe from applying now
        user_id = c.get("user_id")  # original user_id
        logger.debug("user_id={}".format(user_id))
        if not forced and user_id != "" and \
                not user_id.startswith(SYS_DELETER):
            # not forced, then only process unused or in-deleting
            logger.warn("Cannot find deletable cluster {} in {} by "
                        "user {}".format(id, col_name, user_id))
            self.col_active.update_one({"id": id},
                                       {"$set": {"user_id": user_id}})
            return False

        #  0. in db, user_id = SYS_DELETER
        #  1. forced, user_id="", user_id='xxx', or user_id=^SYS_DELETER
        #  2. not forced, user_id == "" or user_id=^SYS_DELETER
        #  Then, add deleting flag to the db, and start deleting
        if not user_id.startswith(SYS_DELETER):
            self.col_active.update_one(
                {"id": id},
                {"$set": {"user_id": SYS_DELETER+user_id}})  # keep user info
        host_id, daemon_url, api_url, consensus_plugin = \
            c.get("host_id"), c.get("daemon_url"), c.get("api_url", ""), \
            c.get("consensus_plugin", CONSENSUS_PLUGINS[0])
        port = api_url.split(":")[-1] or CLUSTER_API_PORT_START
        h = col_host.find_one({"id": host_id})
        if not h:
            logger.warn("No host found with id=" + host_id)
            return False
        has_exception = False
        try:
            compose_stop(name=id, daemon_url=daemon_url, api_port=port,
                         consensus_plugin=consensus_plugin)
        except Exception as e:
            logger.error("Error in stop compose project, will clean")
            logger.debug(e)
            has_exception = True
        try:
            clean_project_containers(daemon_url=daemon_url, name_prefix=id)
        except Exception as e:
            logger.error("Error in clean compose project containers")
            logger.error(e)
            has_exception = True
        try:
            clean_chaincode_images(daemon_url=daemon_url, name_prefix=id)
        except Exception as e:
            logger.error("Error clean chaincode images")
            logger.error(e)
            has_exception = True
        if has_exception:
            logger.warn("Cluster {} delete: stop with exceptions".format(id))
            return False
        col_host.update_one({"id": c.get("host_id")},
                            {"$pull": {"clusters": id}}),
        self.col_active.delete_one({"id": id})
        if record:  # record to release collection
            logger.debug("Record the cluster info into released collection")
            c["release_ts"] = datetime.datetime.now()
            c["duration"] = str(c["release_ts"] - c["apply_ts"])
            # seems mongo reject timedelta type
            if user_id.startswith(SYS_DELETER):
                c["user_id"] = user_id[len(SYS_DELETER):]
            logger.debug(c)
            self.col_released.insert_one(c)
        return True

    def apply_cluster(self, user_id, condition={}, multi_chain=False):
        """ Apply a cluster for a user

        :param user_id: which user will apply the cluster
        :param condition: the filter to select
        :param multi_chain: Allow multiple chain for each tenant
        :return: serialized cluster or None
        """
        if not multi_chain:
            filt = {"user_id": user_id, "release_ts": ""}
            filt.update(condition)
            c = self.col_active.find_one(filt)
            if c:
                logger.debug("Already assigned cluster for " + user_id)
                return self._serialize(c, keys=['id', 'name', 'user_id',
                                                'daemon_url', 'api_url',
                                                'consensus_plugin',
                                                'consensus_mode', 'size'])
        logger.debug("Try find available cluster for " + user_id)
        hosts = col_host.find({"status": "active", "schedulable": "true"})
        host_ids = [h.get("id") for h in hosts]
        logger.debug("Find active and schedulable hosts={}".format(host_ids))
        for h_id in host_ids:  # check each active and schedulable host
            filt = {"user_id": "", "host_id": h_id}
            filt.update(condition)
            c = self.col_active.find_one_and_update(filt,
                {"$set": {"user_id": user_id,
                          "apply_ts": datetime.datetime.now()}},
                return_document=ReturnDocument.AFTER)
            if c and c.get("user_id") == user_id:
                logger.info("Now have cluster {} at {} for user {}".format(
                    c.get("id"), h_id, user_id))
                return self._serialize(c, keys=['id', 'name', 'user_id',
                                                'daemon_url', 'api_url',
                                                'consensus_plugin',
                                                'consensus_mode', 'size'])
        logger.warn("Not find matched available cluster for " + user_id)
        return {}

    def release_cluster_for_user(self, user_id):
        """ Release all cluster for a user_id.

        :param user_id: which user
        :return: True or False
        """
        logger.debug("release clusters for user_id={}".format(user_id))
        c = self.col_active.find({"user_id": user_id, "release_ts": ""})
        cluster_ids = list(map(lambda x: x.get("id"), c))
        logger.debug("clusters for user {}={}".format(user_id, cluster_ids))
        result = True
        for cid in cluster_ids:
            result = result and self.release_cluster(cid)
        return result

    def release_cluster(self, cluster_id):
        """ Release a specific cluster

        Release means delete and try recreating it.

        :param cluster_id: specific cluster to release
        :return: True or False
        """
        c = self.col_active.find_one_and_update(
            {"id": cluster_id, "release_ts": ""},
            {"$set": {"release_ts": datetime.datetime.now()}},
            return_document=ReturnDocument.AFTER)
        if not c or not c.get("release_ts"):  # not have one
            logger.warn("No cluster can be released for id {}".format(
                cluster_id))
            return False

        def delete_recreate_work():
            logger.debug("Run recreate_work in background thread")
            cluster_id, cluster_name, consensus_plugin, consensus_mode, \
            size = \
                c.get("id"), c.get("name"), c.get("consensus_plugin"), \
                c.get("consensus_mode"), c.get("size")
            host_id, api_url = c.get("host_id"), c.get("api_url")
            # h = col_host.find_one({"id": host_id})
            # if not h or h.get("status") != "active":
            #     logger.warn("No host found with id=" + host_id)
            #     return
            if not self.delete(cluster_id, record=True, forced=True):
                logger.warn("Delete cluster failed with id=" + cluster_id)
            else:
                if not self.create(name=cluster_name, host_id=host_id,
                                   api_port=int(api_url.split(":")[-1]),
                                   consensus_plugin=consensus_plugin,
                                   consensus_mode=consensus_mode, size=size):
                    logger.warn("ReCreate cluster failed with name=" +
                                cluster_name)

        t = Thread(target=delete_recreate_work, args=())
        t.start()

        return True

    def _get_active_host(self, id):
        """
        Check if id exists, and status is active. Otherwise update to inactive.

        :param id: host id
        :return: host or None
        """
        logger.debug("check host with id = {}".format(id))
        host = col_host.find_one({"id": id})
        if not host:
            logger.warn("No host found with id=" + id)
            return None
        if host.get("status") != "active":
            logger.warn("Host's status is marked inactive with id=" + id)
            return None
        if not test_daemon(host.get("daemon_url")):
            logger.warn("Host {} is inactive".format(id))
            host = col_host.find_one_and_update(
                {"id": id},
                {"$set": {"status": "inactive"}},
                return_document=ReturnDocument.AFTER)
            return None
        return host

    def _serialize(self, doc, keys=['id', 'name', 'user_id', 'host_id',
                                    'api_url', 'consensus_plugin',
                                    'consensus_mode', 'daemon_url',
                                    'create_ts', 'apply_ts', 'release_ts',
                                    'duration', 'containers', 'size']):
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
        if len(ports_existed) + number >= 10000:
            logger.warn("Too much ports are already used.")
            return []
        candidates = [CLUSTER_API_PORT_START+i for i in range(len(
            ports_existed) + number)]  # 10 is the room for tolerance
        result = [item for item in candidates if item not in ports_existed]

        logger.debug("available ports are:")
        logger.debug(result[:number])
        return result[:number]


# This will be exported as single instance for usage.
cluster_handler = ClusterHandler()