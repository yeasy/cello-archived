import __future__
import os
import sys

import logging
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from common import log_handler
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(log_handler)


# clusters list
class ClustersRoute(Resource):
    def get(self):
        logger.debug("reach ClusterRoute")
        return {}


# A single hyperledger cluster
class ClusterRoute(Resource):
    def get(self, cluster_id):
        return {}

    def post(self, cluster_id):
        args = parser.parse_args()
        return {}, 201

    def delete(self, cluster_id):
        return {}, 204