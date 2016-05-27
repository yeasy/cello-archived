# first port that can be assigned as cluster API
CLUSTER_API_PORT_START = 5000

COMPOSE_FILE_PATH = "./_compose_files"

CLUSTER_NETWORK = "hyperledger_cluster_net"

APP_API_VERSION = "v1"

CONSENSUS_TYPES = ['pbft', 'sieve', 'noops']  # first one is the default one

HOST_TYPES = ['single', 'swarm']
