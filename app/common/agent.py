import logging

from compose.container import Container
from compose.cli.command import get_project as compose_get_project, get_config_path_from_options
from compose.config.config import get_default_config_files
from compose.config.environment import Environment
from docker import Client

from .log import log_handler

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(log_handler)


def clean_chaincode_images(daemon_url, name_prefix):
    client = Client(base_url=daemon_url)
    images = client.images()
    id_removes = [e['Id'] for e in images if e['RepoTags'][0].startswith(
        name_prefix)]
    logger.debug("chaincode image id to removes="+", ".join(id_removes))
    for _ in id_removes:
        client.remove_image(_)

def clean_exited_containers(daemon_url):
    client = Client(base_url=daemon_url)
    containers = client.containers(quiet=True, all=True,
                                   filters={"status": "exited"})
    id_removes = [e['Id'] for e in containers]
    logger.debug("exited container id to removes="+", ".join(id_removes))
    for _ in id_removes:
        client.remove_container(_)

def check_daemon_url(daemon_url):
    """ Check if the daemon is active
    Only wait for 2 seconds.

    :return: bool
    """
    client = Client(base_url=daemon_url, timeout=2)
    try:
        return client.ping() == u'OK'
    except:
        return False


def ps_(project):
    """
    containers status
    """
    containers = project.containers(stopped=True)

    items = [{
        'name': container.name,
        'name_without_project': container.name_without_project,
        'command': container.human_readable_command,
        'state': container.human_readable_state,
        'labels': container.labels,
        'ports': container.ports,
        'volumes': get_volumes(get_container_from_id(project.client, container.id)),
        'is_running': container.is_running} for container in containers]

    return items


def get_container_from_id(client, container_id):
    """
    return the docker container from a given id
    """
    return Container.from_id(client, container_id)

def get_volumes(container):
    """
    retrieve container volumes details
    """
    return container.get('Config.Volumes')


def get_yml_path(path):
    """
    get path of docker-compose.yml file
    """
    return get_default_config_files(path)[0]


def get_project(path):
    """
    get docker project given file path
    """
    environment = Environment.from_env_file(path)
    config_path = get_config_path_from_options(path, dict(), environment)
    project = compose_get_project(path, config_path)
    return project
