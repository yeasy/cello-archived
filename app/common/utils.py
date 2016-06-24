import json
# first port that can be assigned as cluster API
CLUSTER_API_PORT_START = 5000

COMPOSE_FILE_PATH = "./_compose_files"

CLUSTER_NETWORK = "hyperledger_cluster_net"
CLUSTER_SIZES = [4, 6]

APP_API_VERSION = "v1"

CONSENSUS_PLUGINS = ['noops', 'pbft']  # first one is the default one
CONSENSUS_MODES = ['classic', 'batch', 'sieve']  # pbft has various modes

LOG_TYPES = ['local', 'syslog']

HOST_TYPES = ['single', 'swarm']

SYS_CREATOR = "__SYSTEM__CREATING__"
SYS_DELETER = "__SYSTEM__DELETING__"


def json_decode(jsonstr):
    try:
        json_object = json.loads(jsonstr)
    except json.decoder.JSONDecodeError as e:
        print(e)
        return jsonstr
    return json_object


def debug_request(logger, request):
    for k in request.args:
        logger.debug("Arg: {0}:{1}".format(k, request.args[k]))
    for k in request.form:
        logger.debug("Form: {0}:{1}".format(k, request.form[k]))


