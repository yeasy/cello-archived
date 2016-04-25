"""
agent to call docker-compose api
"""

from compose.container import Container
from compose.cli.command import get_project as compose_get_project, get_config_path_from_options
from compose.config.config import get_default_config_files
from compose.config.environment import Environment
from docker.client import Client


def clean_exited_containers(daemon_url):
    client = Client(base_url=daemon_url)
    containers = client.containers(quiet=True, all=True,
                                   filters={"status": "exited"})
    print(containers)
    for c in containers:
        client.remove_container(c)

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
