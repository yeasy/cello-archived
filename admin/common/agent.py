# This module provides some static api to operate compose and docker engine


import logging

from compose.cli.command import get_project as compose_get_project, \
    get_config_path_from_options as compose_get_config_path_from_options
from compose.config.config import get_default_config_files
from compose.config.environment import Environment
from compose.container import Container
from docker import Client

from .log import log_handler, LOG_LEVEL
from .utils import HOST_TYPES

logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
logger.addHandler(log_handler)


def clean_chaincode_images(daemon_url, name_prefix):
    """ Clean chaincode images, whose name should have cluster id as prefix

    :param daemon_url: Docker daemon url
    :param name_prefix: image name prefix
    :return: None
    """
    client = Client(base_url=daemon_url)
    images = client.images()
    id_removes = [e['Id'] for e in images if e['RepoTags'][0].startswith(
        name_prefix)]
    logger.debug("chaincode image id to removes=" + ", ".join(id_removes))
    for _ in id_removes:
        client.remove_image(_)


def clean_exited_containers(daemon_url):
    """ Clean those containers with exited status

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
        client.remove_container(_)


def test_daemon(daemon_url, timeout=2):
    """ Check if the daemon is active

    Only wait for 2 seconds.

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


def detect_daemon_type(daemon_url, timeout=2):
    """ Try to detect the daemon type

    Only wait for 2 seconds.

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
    except:
        return None


def detect_container_host(swarm_url, container_name, timeout=2):
    """
    Detect the host ip where the given container locate in the swarm cluster

    :param swarm_url: Swarm cluster api url
    :param container_name: The container name
    :param timeout: Time to wait for the response
    :return: host ip
    """
    try:
        client = Client(base_url=swarm_url, timeout=timeout)
        info = client.inspect_container(container_name)
        return info['NetworkSettings']['Ports']['5000/tcp'][0]['HostIp']
    except:
        return ''
    pass

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
