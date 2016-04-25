import __future__

import datetime
import logging
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from common import get_project, db, log_handler, get_project, \
    clean_exited_containers

from common.utils import CLUSTER_API_PORT_START

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(log_handler)


class ClusterHandler(object):
    def __init__(self):
        self.collections = db["cluster"]

    def _gen_api_url(self, daemon_url):
        """ Generate an api url automatically.
        :param daemon_url, may look like: tcp://192.168.0.1:2375
        :param d
        """
        logger.info("gen_api_url, daemon_url="+daemon_url)
        segs = daemon_url.split(":")
        if len(segs) != 3:
            logger.error("invalid daemon url = ", daemon_url)
            return ""
        host_ip = segs[1][2:]
        logger.debug("host_ip="+host_ip)
        exists = self.collections.find({"daemon_url": daemon_url})
        api_url_existed = list(map(lambda c: c.get("api_url", ""),
                                   exists))
        logger.warn("api_url_existed:")
        logger.warn(api_url_existed)
        for i in range(len(list(api_url_existed))+1):
            new_url = "http://{0}:{1}".format(host_ip, CLUSTER_API_PORT_START+i)
            logger.debug("new_url="+new_url)
            if new_url not in api_url_existed:
                logger.debug("get new_url="+new_url)
                return new_url
        logger.warn("no valid api_url is generated")
        return ""

    def start_compose_project(self, name, port, daemon_url):
        logger.info("start compose project")
        os.environ['DOCKER_HOST'] = daemon_url
        os.environ['COMPOSE_PROJECT_NAME'] = name
        os.environ['API_URL_PORT'] = port
        project = get_project("./common")
        project.up()

    def stop_compose_project(self, name, port, daemon_url):
        logger.info("stop compose project")
        os.environ['DOCKER_HOST'] = daemon_url
        os.environ['COMPOSE_PROJECT_NAME'] = name
        os.environ['PEER_NETWORKID'] = name
        os.environ['API_URL_PORT'] = port
        project = get_project("./common")
        project.stop()
        project.remove_stopped()

    def clean_containers(self, daemon_url):
        logger.info("clean exited containers")
        clean_exited_containers(daemon_url)

    def list(self):
        logger.info("list all clusters")
        result = map(self._serialize, self.collections.find())
        return result

    def get(self, id):
        logger.info("get a cluster")
        return self.collections.find_one({"id": id})

    def create(self, name, daemon_url, api_url="", user_id=""):
        """ create a cluster based on given data
        TODO: maybe need other id generation mechanism
        TODO: maybe need to check daemon_url status

        :return json obj
        """
        logger.info("create a cluster")
        if not daemon_url.starswith("tcp://"):
            daemon_url = "tcp://" + daemon_url
        if not api_url:  # automatically schedule one
            api_url = self._gen_api_url(daemon_url)
        c = {
                'name': name,
                'user_id': user_id,
                'api_url': api_url,
                'daemon_url': daemon_url,
                'create_ts': datetime.datetime.utcnow(),
                'drop_ts': "",
            }
        ins_id = self.collections.insert_one(c).inserted_id
        self.collections.update({"_id": ins_id}, {"$set":{"id": str(ins_id)}})
        self.start_compose_project(name=str(ins_id),
                                   port=api_url.split(":")[-1],
                                   daemon_url=daemon_url)

    def delete(self, id):
        logger.info("delete a cluster with id="+id)
        ins = self.collections.find_one({"id": id})
        if not ins:
            logger.warn("Cannot delete unexisted instance")
            return
        api_url = ins.get("api_url", "")
        daemon_url = ins.get("daemon_url", "")
        self.stop_compose_project(name=id,
                                  port=api_url.split(":")[-1],
                                  daemon_url=daemon_url)
        self.clean_containers(daemon_url)
        self.collections.delete_one({"id": id})

    def find_free(self):
        """
        Find a free to use cluster
        """
        result = self.collections.find_one({"user_id": ""})
        result['apply_ts'] = datetime.datetime.utcnow(),
        return self._serialize(result)

    def set_user_id(self, doc, user_id):
        """
        Set the user_id value to given doc
        """
        return self.collections.update({"id": doc.get('id','')},
                                       {"$set": {"user_id": user_id}})

    def _serialize(self, doc):
        return {
            'id': doc.get('id', ''),
            'name': doc.get('name', ''),
            'user_id': doc.get('user_id', ''),
            'api_url': doc.get('api_url', ''),
            'daemon_url': doc.get('daemon_url', ''),
            'create_ts': doc.get('create_ts', ''),
            'apply_ts': doc.get('apply_ts', ''),
            'drop_ts': doc.get('drop_ts', ''),
        }

cluster_handler = ClusterHandler()