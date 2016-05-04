import datetime
import logging
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from common import db, log_handler, LOG_LEVEL, get_project, \
    clean_exited_containers, clean_chaincode_images, check_daemon_url, \
    CLUSTER_API_PORT_START, COMPOSE_FILE_PATH

logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)

class HostHandler(object):
    """ Main handler to operate the Docker hosts

    """
    def __init__(self):
        self.collections = db["host"]

    def create(self, name, daemon_url, status="active"):
        """ Create a new docker host node

        :param name: name of the node
        :param daemon_url: daemon_url of the cluster
        :param status: active for using, inactive for not using
        :return: True or False
        """
        logger.debug("Create new host with name={0}, daemon_url={"
                     "1}".format(name, daemon_url))
        if not daemon_url.startswith("tcp://"):
            daemon_url = "tcp://" + daemon_url
        if not check_daemon_url(daemon_url):
            logger.warn("The daemon_url is not valid:" + daemon_url)
            return False
        h = {
            'name': name,
            'daemon_url': daemon_url,
            'create_ts': datetime.datetime.now(),
        }
        ins_id = self.collections.insert_one(h).inserted_id  # object type
        self.collections.update({"_id": ins_id}, {"$set": {"id": str(ins_id)}})
        return True

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
        self.collection.delete_one({"id": id})
        return True


host_handler = HostHandler()