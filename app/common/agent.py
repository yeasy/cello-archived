# This module provides some static api to operate compose and docker engine


import logging
import os

from compose.cli.command import get_project as compose_get_project, \
    get_config_path_from_options as compose_get_config_path_from_options
from compose.config.config import get_default_config_files
from compose.config.environment import Environment
from compose.container import Container
from compose.project import OneOffFilter
from docker import Client

from .log import log_handler, LOG_LEVEL
from .utils import HOST_TYPES, CLUSTER_API_PORT_START, CLUSTER_NETWORK, COMPOSE_FILE_PATH, CONSENSUS_TYPES

logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
logger.addHandler(log_handler)


def clean_chaincode_images(daemon_url, name_prefix, timeout=5):
    """ Clean chaincode images, whose name should have cluster id as prefix

    :param daemon_url: Docker daemon url
    :param name_prefix: image name prefix
    :param timeout: Time to wait for the response
    :return: None
    """
    logger.debug("clean chaincode images with prefix={}".format(name_prefix))
    client = Client(base_url=daemon_url, timeout=timeout)
    images = client.images()
    id_removes = [e['Id'] for e in images if e['RepoTags'][0].startswith(
        name_prefix)]
    logger.debug("chaincode image id to removes=" + ", ".join(id_removes))
    for _ in id_removes:
        client.remove_image(_, force=True)


def clean_project_containers(daemon_url, name_prefix, timeout=5):
    """
    Clean cluster node containers and chaincode containers

    All containers with the name prefix will be removed.

    :param daemon_url: Docker daemon url
    :param name_prefix: image name prefix
    :param timeout: Time to wait for the response
    :return: None
    """
    logger.debug("Clean project related containers")
    client = Client(base_url=daemon_url, timeout=timeout)
    containers = client.containers(all=True)
    id_removes = [e['Id'] for e in containers if e['Names'][0][
                                                 1:].startswith(name_prefix)]
    for _ in id_removes:
        logger.debug("Remove container "+_)
        client.remove_container(_, force=True)


#  Deprecated
#  Normal chaincode container may also become exited temporarily
def clean_exited_containers(daemon_url):
    """ Clean those containers with exited status

    This is dangerous, as it may delete temporary containers.
    Only trigger this when no one else uses the system.

    :param daemon_url: Docker daemon url
    :return: None
    """
    logger.debug("Clean exited containers")
    client = Client(base_url=daemon_url)
    containers = client.containers(quiet=True, all=True,
                                   filters={"status": "exited"})
    id_removes = [e['Id'] for e in containers]
    for _ in id_removes:
        logger.debug("exited container id to removes="+_)
        try:
            client.remove_container(_)
        except Exception as e:
            logger.error("Exception in clean_exited_containers")
            logger.error(e)


def test_daemon(daemon_url, timeout=5):
    """ Check if the daemon is active

    Only wait for timeout seconds.

    :param daemon_url: Docker daemon url
    :param timeout: Time to wait for the response
    :return: True for active, False for inactive
    """
    if not daemon_url or not daemon_url.startswith("tcp://"):
        return False
    segs = daemon_url.split(":")
    if len(segs) != 3:
        logger.error("Invalid daemon url = ", daemon_url)
        return False
    try:
        client = Client(base_url=daemon_url, timeout=timeout)
        return client.ping() == 'OK'
    except:
        return False


def detect_daemon_type(daemon_url, timeout=5):
    """ Try to detect the daemon type

    Only wait for timeout seconds.

    :param daemon_url: Docker daemon url
    :param timeout: Time to wait for the response
    :return: host type info
    """
    if not daemon_url or not daemon_url.startswith("tcp://"):
        return None
    segs = daemon_url.split(":")
    if len(segs) != 3:
        logger.error("Invalid daemon url = ", daemon_url)
        return None
    try:
        client = Client(base_url=daemon_url, timeout=timeout)
        server_version = client.info()['ServerVersion']
        if server_version.startswith('swarm'):
            return 'swarm'
        else:
            return 'single'
    except Exception as e:
        logger.error(e)
        return None


def reset_container_host(daemon_url, timeout=15):
    """ Try to detect the daemon type

    Only wait for timeout seconds.

    :param daemon_url: Docker daemon url
    :param timeout: Time to wait for the response
    :return: host type info
    """
    try:
        client = Client(base_url=daemon_url, timeout=timeout)
        containers = client.containers(quiet=True, all=True)
        logger.debug(containers)
        for c in containers:
            client.remove_container(c['Id'], force=True)
        logger.debug("cleaning all containers")
    except Exception as e:
        logger.error("Exception happens when reset host!")
        logger.error(e)
        return False
    try:
        images = client.images(all=True)
        logger.debug(images)
        for i in images:
            if i["RepoTags"][0] == "<none>:<none>":
                logger.debug(i)
                try:
                    client.remove_image(i['Id'])
                except Exception as e:
                    logger.error(e)
                    continue
        logger.debug("cleaning <none> images")
        return True
    except Exception as e:
        logger.error("Exception happens when reset host!")
        logger.error(e)
        return False


def detect_container_host(swarm_url, container_name, timeout=5):
    """
    Detect the host ip where the given container locate in the swarm cluster

    :param swarm_url: Swarm cluster api url
    :param container_name: The container name
    :param timeout: Time to wait for the response
    :return: host ip
    """
    logger.debug("Detect container={} with swarm_url={}".format(
        container_name, swarm_url))
    try:
        client = Client(base_url=swarm_url, timeout=timeout)
        info = client.inspect_container(container_name)
        return info['NetworkSettings']['Ports']['5000/tcp'][0]['HostIp']
    except:
        return ''

def setup_container_host(host_type, daemon_url, timeout=5):
    """
    Setup a container host for deploying cluster on it

    :param host_type: Docker host type
    :param daemon_url: Docker daemon url
    :param timeout: timeout to wait
    :return: True or False
    """
    if not daemon_url or not daemon_url.startswith("tcp://"):
        logger.error("Invalid daemon_url={}".format(daemon_url))
        return False
    if host_type not in HOST_TYPES:
        logger.error("Invalid host_type={}".format(host_type))
        return False
    try:
        client = Client(base_url=daemon_url, timeout=timeout)
        for cs_type in CONSENSUS_TYPES:
            net_name = CLUSTER_NETWORK+"_{}".format(cs_type)
            net_names = client.networks(names=[net_name])
            if net_names:
                logger.warn("Network {} already exists, try using "
                            "it!".format(net_name))
            else:
                if host_type == HOST_TYPES[0]:  # single
                    client.create_network(net_name, driver='bridge')
                elif host_type == HOST_TYPES[1]:  # swarm
                    client.create_network(net_name, driver='overlay')
                else:
                    logger.error("No-supported host_type={}".format(host_type))
                    return False
    except Exception as e:
        logger.error("Exception happens!")
        logger.error(e)
        return False
    return True


def cleanup_container_host(daemon_url, timeout=5):
    """
    Cleanup a container host when use removes the host

    Maybe we will remove the networks?

    :param host_type: Docker host type
    :param daemon_url: Docker daemon url
    :param timeout: timeout to wait
    :return:
    """
    if not daemon_url or not daemon_url.startswith("tcp://"):
        logger.error("Invalid daemon_url={}".format(daemon_url))
        return False
    try:
        client = Client(base_url=daemon_url, timeout=timeout)
        for cs_type in CONSENSUS_TYPES:
            net_name = CLUSTER_NETWORK+"_{}".format(cs_type)
            net_names = client.networks(names=[net_name])
            if net_names:
                logger.debug("Remove network {}".format(net_name))
                client.remove_network(net_name)
            else:
                logger.warn("Network {} not exists!".format(net_name))
    except Exception as e:
        logger.error("Exception happens!")
        logger.error(e)
        return False
    return True


def get_project(template_path):
    """ Get compose project with given template file path

    :param template_path: path of the compose template file
    :return: project object
    """
    environment = Environment.from_env_file(template_path)
    config_path = compose_get_config_path_from_options(template_path, dict(),
                                                       environment)
    project = compose_get_project(template_path, config_path)
    return project


# no used
def compose_ps(project):
    """ Get containers status of given compose project

    :param project: Project to operate
    :return: Those container information in dict
    """
    containers = project.containers(stopped=True)

    items = [{
                 'name': container.name,
                 'name_without_project': container.name_without_project,
                 'command': container.human_readable_command,
                 'state': container.human_readable_state,
                 'labels': container.labels,
                 'ports': container.ports,
                 'volumes': get_volumes(
                     get_container_from_id(project.client, container.id)),
                 'is_running': container.is_running} for container in
             containers]

    return items


def compose_start(name, api_port, daemon_url,
                  consensus_type=CONSENSUS_TYPES[0],timeout=5):
    """ Start a cluster by compose

    :param name: The name of the cluster
    :param api_port: The port of the cluster API
    :param daemon_url: Docker host daemon
    :param consensus_type: Cluster consensus type
    :param timeout: Docker client timeout value
    :return: The name list of the started peer containers
    """
    logger.debug("Start compose project with logging_level={}, "
                 "consensus={}".format(os.environ['LOGGING_LEVEL_CLUSTER'],
                                       consensus_type))
    os.environ['DOCKER_HOST'] = daemon_url   # start compose at which host
    os.environ['DAEMON_URL'] = daemon_url  # vp use this for chaincode
    os.environ['COMPOSE_PROJECT_NAME'] = name
    os.environ['PEER_NETWORKID'] = name
    os.environ['API_PORT'] = str(api_port)
    os.environ['CLUSTER_NETWORK'] = CLUSTER_NETWORK+"_{}".format(consensus_type)
    project = get_project(COMPOSE_FILE_PATH+"/"+consensus_type)
    containers = project.up(detached=True, timeout=timeout)
    result = {}
    for c in containers:
        result[c.name] = c.id
    logger.debug("compose started with containers={}".format(result))
    return result


def compose_stop(name, daemon_url, api_port=CLUSTER_API_PORT_START,
                 consensus_type=CONSENSUS_TYPES[0], timeout=5):
    """ Stop the cluster and remove the service containers

    :param name: The name of the cluster
    :param daemon_url: Docker host daemon
    :param api_port: The port of the cluster API
    :param logging_level: logging level for the cluster output
    :param consensus_type: Cluster consensus type
    :param timeout: Docker client timeout
    :return:
    """
    logger.debug("Stop compose project {} with logging_level={}, "
                 "consensus={}".format(name, os.environ[
        'LOGGING_LEVEL_CLUSTER'], consensus_type))
    os.environ['DOCKER_HOST'] = daemon_url
    os.environ['DAEMON_URL'] = daemon_url  # vp use this for chaincode
    os.environ['COMPOSE_PROJECT_NAME'] = name
    os.environ['PEER_NETWORKID'] = name
    os.environ['API_PORT'] = str(api_port)
    os.environ['CLUSTER_NETWORK'] = CLUSTER_NETWORK+"_{}".format(consensus_type)
    project = get_project(COMPOSE_FILE_PATH+"/"+consensus_type)
    project.stop(timeout=timeout)
    project.remove_stopped(one_off=OneOffFilter.include, force=True)


# no used
def get_container_from_id(client, container_id):
    """
    return the docker container from a given id
    """
    return Container.from_id(client, container_id)


# no used
def get_volumes(container):
    """
    retrieve container volumes details
    """
    return container.get('Config.Volumes')


# no used
def get_yml_path(path):
    """
    get path of docker-compose.yml file
    """
    return get_default_config_files(path)[0]
