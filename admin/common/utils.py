import json
import os

# first port that can be assigned as cluster API
CLUSTER_API_PORT_START = int(os.getenv("CLUSTER_API_PORT_START", 5000))

COMPOSE_FILE_PATH = os.getenv("COMPOSE_FILE_PATH", "./_compose_files")

CLUSTER_NETWORK = "bpm_net"
CLUSTER_SIZES = [4, 6]

CONSENSUS_PLUGINS = ['noops', 'pbft']  # first one is the default one
# CONSENSUS_MODES = ['classic', 'batch', 'sieve']  # pbft has various modes
CONSENSUS_MODES = ['batch']  # pbft has various modes

CONSENSUS_TYPES = [
    ('noops', ''),
    ('pbft', 'batch'),
    #('pbft', 'classic'),
    #('pbft', 'sieve'),
]

LOG_TYPES = ['local', 'syslog']

HOST_TYPES = ['single', 'swarm']

LOGGING_LEVEL_CLUSTERS = ['DEBUG', 'INFO', 'NOTICE', 'WARNING', 'ERROR',
                         'CRITICAL']

SYS_CREATOR = "__SYSTEM__CREATING__"
SYS_DELETER = "__SYSTEM__DELETING__"


def json_decode(jsonstr):
    try:
        json_object = json.loads(jsonstr)
    except json.decoder.JSONDecodeError as e:
        print(e)
        return jsonstr
    return json_object


def request_debug(request, logger):
    logger.debug("path={}, method={}".format(request.path, request.method))
    logger.debug("request args:")
    for k in request.args:
        logger.debug("Arg: {0}:{1}".format(k, request.args[k]))
    logger.debug("request form:")
    for k in request.form:
        logger.debug("Form: {0}:{1}".format(k, request.form[k]))
    logger.debug("request raw body data:")
    logger.debug(request.data)


def request_get(request, key, default_value=None):
    if key in request.args:
        return request.args.get(key)
    elif key in request.form:
        return request.form.get(key)
    try:
        json_body = request.get_json(force=True, silent=True)
        if key in json_body:
            return json_body[key]
        else:
            return default_value
    except Exception as e:
        return default_value


def request_json_body(request, default_value={}):
    try:
        json_body = request.get_json(force=True, silent=True)
        return json_body
    except Exception as e:
        return default_value