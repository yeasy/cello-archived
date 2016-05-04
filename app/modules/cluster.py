import datetime
import logging
import os
import sys

from threading import Thread

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from common import db, log_handler, LOG_LEVEL, get_project, \
    clean_exited_containers, clean_chaincode_images, check_daemon_url, \
    CLUSTER_API_PORT_START, COMPOSE_FILE_PATH

logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
logger.addHandler(log_handler)


class ClusterHandler(object):
    """ Main handler to operate the cluster in pool

    """
    def __init__(self):
        self.collections_active = db["cluster_active"]
        self.collections_released = db["cluster_released"]

    def _compose_start_project(self, name, port, daemon_url):
        """ Start a compose project

        :param name: The name of the cluster
        :param port: The port of the cluster API
        :param daemon_url: Docker host daemon
        :return: The name list of the started peer containers
        """
        logger.debug("Start compose project")
        os.environ['DOCKER_HOST'] = daemon_url
        os.environ['COMPOSE_PROJECT_NAME'] = name
        os.environ['PEER_NETWORKID'] = name
        os.environ['API_URL_PORT'] = port
        project = get_project(COMPOSE_FILE_PATH)
        containers = project.up(detached=True)
        return [c.get('Name')[1:] for c in containers]

    def _compose_stop_project(self, name, port, daemon_url):
        """ Stop a compose project

        :param name: The name of the cluster
        :param port: The port of the cluster API
        :param daemon_url: Docker host daemon
        :return:
        """
        logger.debug("Stop compose project "+name)
        os.environ['DOCKER_HOST'] = daemon_url
        os.environ['COMPOSE_PROJECT_NAME'] = name
        os.environ['PEER_NETWORKID'] = name
        os.environ['API_URL_PORT'] = port
        project = get_project(COMPOSE_FILE_PATH)
        project.stop()
        project.remove_stopped()

    def _clean_containers(self, daemon_url):
        """

        :param daemon_url: Docker host daemon
        :return:
        """
        logger.debug("Clean exited containers")
        clean_exited_containers(daemon_url)

    def _clean_images(self, daemon_url, name_prefix):
        """ Clean unused images.

        Image with given name prefix will be removed.

        :param daemon_url:
        :param name_prefix:
        :return:
        """
        logger.debug("Clean chaincode images")
        clean_chaincode_images(daemon_url, name_prefix)

    def list(self, filter_data={}, collection="active"):
        """ List clusters with given criteria

        :param filter_data: Image with the filter properties
        :param collection: Use data in which collection
        :return: iteration of serialized doc
        """
        if collection == "active":
            logger.debug("List all active clusters")
            result = map(self._serialize, self.collections_active.find(filter_data))
        elif collection == "released":
            logger.debug("List all released clusters")
            result = map(self._serialize, self.collections_released.find(
                filter_data))
        else:
            logger.warn("Unknown cluster collection="+collection)
            return None
        return result

    def get(self, id, serialization=False, collection=""):
        """ Get a cluster

        :param id: id of the doc
        :param serialization: whether to get serialized result or object
        :param collection: collection to check
        :return: serialized result or obj
        """
        if collection != "released":
            logger.debug("Get a cluster with id=" + id)
            ins = self.collections_active.find_one({"id": id})
        else:
            logger.debug("Get a released cluster with id=" + id)
            ins = self.collections_released.find_one({"id": id})
        if not ins:
            logger.warn("No cluster found with id=" + id)
            return {}
        if serialization:
            return self._serialize(ins)
        else:
            return ins

    def create(self, name="test", daemon_url="", api_url="", user_id=""):
        """ Create a cluster based on given data
        TODO: maybe need other id generation mechanism

        :param name: name of the cluster
        :param daemon_url: daemon_url of the cluster
        :param api_url: cluster has specific api_url, will generate
        automatically if not given
        :param user_id: user_id of the cluster
        :return: True or False
        """
        logger.debug("Create new cluster with name={0}, daemon_url={"
                     "1}".format(name, daemon_url))
        if not daemon_url.startswith("tcp://"):
            daemon_url = "tcp://" + daemon_url
        if not check_daemon_url(daemon_url):
            logger.warn("The daemon_url is not valid:" + daemon_url)
            return False
        if not api_url:  # automatically schedule one
            api_url = self._gen_api_url(daemon_url)
        c = {
            'name': name,
            'user_id': user_id,
            'api_url': api_url,
            'daemon_url': daemon_url,
            'create_ts': datetime.datetime.now(),
            'release_ts': "",
        }
        ins_id = self.collections_active.insert_one(c).inserted_id  # object type
        try:
            container = self._compose_start_project(name=str(ins_id),
                                                    port=
                                                    api_url.split(":")[-1],
                                                    daemon_url=daemon_url)
        except Exception as e:
            logger.warn(e)
            logger.warn("Remove unsuccessful started cluster info")
            self.collections_active.delete_one({"_id": ins_id})
            return False
        self.collections_active.update({"_id": ins_id}, {"$set": {"id": str(
            ins_id), "node_containers": container}})
        return True

    def delete(self, id, col_name="active", record=False):
        """ Delete a cluster instance

        :param id: id of the cluster to delete
        :param col_name: name of the cluster to operate
        :param record: Whether to record into the released collections
        :return:
        """
        logger.debug("Delete a cluster with id={0}, col_name={1}".format(id,
                                                                         col_name))
        if col_name == "active":
            collection = self.collections_active
        else:
            collection = self.collections_released

        ins = collection.find_one({"id": id})
        if not ins:
            logger.warn("Cannot delete non-existed instance")
            return False
        if col_name == "active":  # stop running containers when active
            api_url = ins.get("api_url", "")
            daemon_url = ins.get("daemon_url", "")
            try:
                self._compose_stop_project(name=id,
                                           port=api_url.split(":")[-1],
                                           daemon_url=daemon_url)
                self._clean_containers(daemon_url)
                self._clean_images(daemon_url=daemon_url, name_prefix=id)
            except Exception as e:
                logger.warn("Wrong in clean compose project and containers")
                logger.warn(e)
                return False
            if record:
                ins["release_ts"] = datetime.datetime.now()
                logger.debug("Record the cluster info into released collection")
                self.collections_released.insert_one(ins)
        collection.delete_one({"id": id})
        return True

    def apply_cluster(self, user_id):
        """ Apply a cluster for a user

        :param user_id: which user will apply the cluster
        :return: serialized cluster
        """
        doc = self.collections_active.find_one({"user_id": user_id})
        if doc:  # already have one
            logger.debug("Already assigned cluster for " + user_id)
            logger.debug(self._serialize(doc, keys=['id', 'name', 'user_id',
                                                    'api_url']))
            return self._serialize(doc, keys=['id', 'name', 'user_id',
                                              'api_url'])
        free_one = self.collections_active.find_one({"user_id": ""})
        if not free_one:
            logger.warn("Not find free one for " + user_id)
            return {}
        else:
            free_one["user_id"] = user_id
            free_one["apply_ts"] = datetime.datetime.now()
            self.collections_active.update({"id": free_one.get('id', '')},
                                           {"$set": {"user_id": free_one["user_id"],
                                              "apply_ts": free_one[
                                                  "apply_ts"]}})
            logger.info("Assign free one for" + user_id)
            logger.info(self._serialize(free_one))
            return self._serialize(free_one, keys=['id', 'name', 'user_id',
                                                   'api_url'])

    def release_cluster(self, user_id):
        """ Release a cluster for a user_id and recreate it.

        :param user_id: which user will apply the cluster
        :return: True or False
        """
        result = self.collections_active.find_one({"user_id": user_id})
        if not result:  # not have one
            logger.warn("There is no cluster for {}".format(user_id))
            return False

        def delete_recreate_work():
            logger.debug("Run recreate_work in background thread")
            cluster_id = result.get("id", "")
            cluster_name = result.get("name", "")
            cluster_daemon_url = result.get("daemon_url", "")
            cluster_api_url = result.get("api_url", "")
            logger.debug("Delete cluster with id=" + cluster_id)
            if not self.delete(cluster_id, record=True):
                logger.warn("Delete cluster error with id=" + cluster_id)
            logger.warn("Recreate cluster with name=" + cluster_name)
            if not self.create(cluster_name, cluster_daemon_url,
                               cluster_api_url):
                logger.warn("Create cluster error with name=" + cluster_name)

        t = Thread(target=delete_recreate_work, args=())
        t.start()

        return True

    def _serialize(self, doc, keys=['id', 'name', 'user_id', 'daemon_url',
                                    'api_url',
                                    'create_ts', 'apply_ts', 'release_ts',
                                    'node_containers']):
        """ Serialize an obj

        :param doc: doc to serialize
        :param keys: filter which key in the results
        :return: serialized obj
        """
        result = {}
        for k in keys:
            result[k] = doc.get(k, '')
        return result

    def _gen_api_url(self, daemon_url):
        """ Generate an api url automatically

        :param daemon_url, may look like: tcp://192.168.0.1:2375
        :return: The generated api url address
        """
        logger.debug("Generate api_url, daemon_url=" + daemon_url)
        segs = daemon_url.split(":")
        if len(segs) != 3:
            logger.error("Invalid daemon url = ", daemon_url)
            return ""
        host_ip = segs[1][2:]
        logger.debug("The host_ip=" + host_ip)
        exists = self.collections_active.find({"daemon_url": daemon_url})
        api_url_existed = list(map(lambda c: c.get("api_url", ""),
                                   exists))
        logger.debug("The api_url_existed:")
        logger.debug(api_url_existed)
        for i in range(len(list(api_url_existed)) + 1):
            new_url = "http://{0}:{1}".format(host_ip,
                                              CLUSTER_API_PORT_START + i)
            logger.debug("Try new_url=" + new_url)
            if new_url not in api_url_existed:
                logger.debug("Get valid new_url=" + new_url)
                return new_url
        logger.warn("No valid api_url is generated")
        return ""


# This will be exported as single instance for usage.
cluster_handler = ClusterHandler()
