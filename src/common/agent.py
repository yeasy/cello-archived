# This module provides some static api to operate compose and docker engine

import logging
import os

from compose.cli.command import get_project as compose_get_project, \
    get_config_path_from_options as compose_get_config_path_from_options
from compose.config.environment import Environment
from compose.project import OneOffFilter
from docker import Client

from .log import log_handler, LOG_LEVEL
from .utils import HOST_TYPES, CLUSTER_API_PORT_START, CLUSTER_NETWORK, \
    COMPOSE_FILE_PATH, CONSENSUS_PLUGINS, CONSENSUS_MODES, LOG_TYPES, \
    CLUSTER_SIZES

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
    logger.debug("Clean project containers, daemon_url={}, prefix={}".format(
        daemon_url, name_prefix))
    client = Client(base_url=daemon_url, timeout=timeout)
    containers = client.containers(all=True)
    id_removes = [e['Id'] for e in containers if
                  e['Names'][0].split("/")[-1].startswith(name_prefix)]
    for _ in id_removes:
        client.remove_container(_, force=True)
        logger.debug("Remove container {}".format(_))


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
        logger.debug("exited container to remove, id={}", _)
        try:
            client.remove_container(_)
        except Exception as e:
            logger.error("Exception in clean_exited_containers")
            logger.error(e)


def check_daemon(daemon_url, timeout=5):
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


def reset_container_host(host_type, daemon_url, timeout=15):
    """ Try to detect the daemon type

    Only wait for timeout seconds.

    :param host_type: Type of host: single or swarm
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
    except Exception as e:
        logger.error("Exception happens when reset host!")
        logger.error(e)
        return False

    return setup_container_host(host_type=host_type, daemon_url=daemon_url)


def get_swarm_node_ip(swarm_url, container_name, timeout=5):
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
    except Exception as e:
        logger.error("Exception happens when detect container host!")
        logger.error(e)
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
        net_names = [x["Name"] for x in client.networks()]
        for cs_type in CONSENSUS_PLUGINS:
            net_name = CLUSTER_NETWORK + "_{}".format(cs_type)
            if net_name in net_names:
                logger.warn("Network {} already exists, try using it!".format(
                    net_name))
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

    :param daemon_url: Docker daemon url
    :param timeout: timeout to wait
    :return:
    """
    if not daemon_url or not daemon_url.startswith("tcp://"):
        logger.error("Invalid daemon_url={}".format(daemon_url))
        return False
    try:
        client = Client(base_url=daemon_url, timeout=timeout)
        net_names = [x["Name"] for x in client.networks()]
        for cs_type in CONSENSUS_PLUGINS:
            net_name = CLUSTER_NETWORK + "_{}".format(cs_type)
            if net_name in net_names:
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


def compose_start(name, host, api_port,
                  consensus_plugin=CONSENSUS_PLUGINS[0],
                  consensus_mode=CONSENSUS_MODES[0],
                  cluster_size=CLUSTER_SIZES[0],
                  timeout=5):
    """ Start a cluster by compose

    :param name: The name of the cluster
    :param api_port: The port of the cluster API
    :param host: Docker host obj
    :param consensus_plugin: Cluster consensus plugin
    :param consensus_mode: Cluster consensus mode
    :param cluster_size: the size of the cluster
    :param timeout: Docker client timeout value
    :return: The name list of the started peer containers
    """
    logger.debug("Compose start: host={}, logging_level={}, "
                 "consensus={}/{}, size={}".format(host.get("name"),
                                                   host.get('log_level'),
                                                   consensus_plugin,
                                                   consensus_mode,
                                                   cluster_size)
                 )
    daemon_url, log_type, log_server = \
        host.get("daemon_url"), host.get("log_type"), host.get("log_server")
    # compose use this
    os.environ['DOCKER_HOST'] = daemon_url  # start compose at which host
    os.environ['COMPOSE_PROJECT_NAME'] = name
    os.environ['COMPOSE_FILE'] = "cluster-{}.yml".format(cluster_size)

    # hyperledger use this
    os.environ['VM_ENDPOINT'] = daemon_url  # vp use this for chaincode
    os.environ['VM_DOCKER_HOSTCONFIG_NETWORKMODE'] = \
        CLUSTER_NETWORK + "_{}".format(consensus_plugin)  # "host"
    # os.environ['VM_DOCKER_HOSTCONFIG_NETWORKMODE'] = "bridge"
    os.environ['PEER_VALIDATOR_CONSENSUS_PLUGIN'] = consensus_plugin
    os.environ['PBFT_GENERAL_MODE'] = consensus_mode
    os.environ['PBFT_GENERAL_N'] = str(cluster_size)
    os.environ['PEER_NETWORKID'] = name
    os.environ['API_PORT'] = str(api_port)
    os.environ['CLUSTER_NETWORK'] = CLUSTER_NETWORK + "_{}".format(
        consensus_plugin)
    os.environ['LOGGING_LEVEL_CLUSTERS'] = host.get("log_level")
    # project = get_project(COMPOSE_FILE_PATH+"/"+consensus_plugin)
    if log_type != LOG_TYPES[0]:  # not local
        os.environ['SYSLOG_SERVER'] = log_server

    try:
        project = get_project(COMPOSE_FILE_PATH + "/" + log_type)
        containers = project.up(detached=True, timeout=timeout)
    except Exception as e:
        logger.warning("Exception when compose start={}".format(e))
        return {}
    if not containers or cluster_size != len(containers):
        return {}
    result = {}
    for c in containers:
        result[c.name] = c.id
    logger.debug("compose started with containers={}".format(result))
    return result


def compose_clean(name, daemon_url, port, consensus_plugin):
    """
    Try best to clean a compose project and clean related containers.

    :param name: name of the project
    :param daemon_url: Docker Host url
    :param port: Which api port
    :param consensus_plugin: which consensus plugin
    :return: True or False
    """
    has_exception = False
    try:
        compose_remove(name=name, daemon_url=daemon_url, api_port=port,
                       consensus_plugin=consensus_plugin)
    except Exception as e:
        logger.error("Error in stop compose project, will clean")
        logger.debug(e)
        has_exception = True
    try:
        clean_project_containers(daemon_url=daemon_url, name_prefix=name)
    except Exception as e:
        logger.error("Error in clean compose project containers")
        logger.error(e)
        has_exception = True
    try:
        clean_chaincode_images(daemon_url=daemon_url, name_prefix=name)
    except Exception as e:
        logger.error("Error clean chaincode images")
        logger.error(e)
        # has_exception = True  # may ignore this case
    if has_exception:
        logger.warning("Exception when cleaning project {}".format(name))
        return False
    return True


def compose_remove(name, daemon_url, api_port=CLUSTER_API_PORT_START,
                   consensus_plugin=CONSENSUS_PLUGINS[0],
                   consensus_mode=CONSENSUS_MODES[0],
                   log_type=LOG_TYPES[0], log_server="",
                   cluster_size=CLUSTER_SIZES[0], timeout=5):
    """ Stop the cluster and remove the service containers

    :param name: The name of the cluster
    :param daemon_url: Docker host daemon
    :param api_port: The port of the cluster API
    :param consensus_plugin: Cluster consensus type
    :param consensus_mode: Cluster consensus mode
    :param log_type: which log plugin for host
    :param log_server: syslog server
    :param cluster_size: the size of the cluster
    :param timeout: Docker client timeout
    :return:
    """
    logger.debug("Stop compose project {} with logging_level={}, "
                 "consensus={}".format(name, 'INFO', consensus_plugin))
    # compose use this
    os.environ['DOCKER_HOST'] = daemon_url
    os.environ['COMPOSE_PROJECT_NAME'] = name
    os.environ['COMPOSE_FILE'] = "cluster-{}.yml".format(cluster_size)

    # hyperledger use this
    os.environ['VM_ENDPOINT'] = daemon_url  # vp use this for chaincode
    os.environ['VM_DOCKER_HOSTCONFIG_NETWORKMODE'] = CLUSTER_NETWORK + "_{}".\
        format(consensus_plugin)  # "host"
    os.environ['PEER_VALIDATOR_CONSENSUS_PLUGIN'] = consensus_plugin
    os.environ['PBFT_GENERAL_MODE'] = consensus_mode
    os.environ['PBFT_GENERAL_N'] = str(cluster_size)
    os.environ['PEER_NETWORKID'] = name
    os.environ['API_PORT'] = str(api_port)
    os.environ['CLUSTER_NETWORK'] = CLUSTER_NETWORK + "_{}".format(
        consensus_plugin)
    os.environ['LOGGING_LEVEL_CLUSTERS'] = "INFO"
    if log_type != LOG_TYPES[0]:  # not local
        os.environ['SYSLOG_SERVER'] = log_server

    # project = get_project(COMPOSE_FILE_PATH+"/"+consensus_plugin)
    project = get_project(COMPOSE_FILE_PATH + "/" + log_type)
    project.stop(timeout=timeout)
    project.remove_stopped(one_off=OneOffFilter.include, force=True)
