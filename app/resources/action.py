from flask import Blueprint, request, jsonify

import logging

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from common import log_handler, LOG_LEVEL, APP_API_VERSION, \
    status_response_ok, status_response_fail, CODE_OK, CODE_CREATED, CODE_BAD_REQUEST, \
    CODE_NO_CONTENT, CONSENSUS_TYPES

from modules import cluster_handler
logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
logger.addHandler(log_handler)

action = Blueprint('action', __name__, url_prefix='/{}'.format(APP_API_VERSION))


@action.route('/cluster_apply', methods=['GET'])
def cluster_apply():
    """
    Return a Cluster json body.
    """
    user_id = request.args.get("user_id", "")
    consensus_type = request.args.get("consensus_type", CONSENSUS_TYPES[0])
    logger.debug("userid="+user_id)
    for k in request.args:
        logger.debug("Arg: {0}:{1}".format(k, request.args[k]))
    for k in request.form:
        logger.debug("Form: {0}:{1}".format(k, request.form[k]))
    if not user_id:
        logger.warn("cluster_apply without user_id")
        status_response_fail["error"] = "No user_id is given"
        status_response_fail["data"] = request.args
        return jsonify(status_response_fail), CODE_BAD_REQUEST
    else:
        c = cluster_handler.apply_cluster(user_id=user_id,consensus_type=consensus_type)
        if not c:
            logger.warn("cluster_apply failed")
            status_response_fail["error"] = "No available res for "+user_id
            status_response_fail["data"] = request.args
            return jsonify(status_response_fail), CODE_BAD_REQUEST
        else:
            return jsonify(c), CODE_OK


@action.route('/cluster_release', methods=['GET'])
def cluster_release():
    """
    Return status.
    """
    user_id = request.args.get("user_id", "")
    logger.debug("userid="+user_id)
    for k in request.args:
        logger.debug("Arg: {0}:{1}".format(k, request.args[k]))
    for k in request.form:
        logger.debug("Form: {0}:{1}".format(k, request.form[k]))
    if not user_id:
        logger.warn("cluster_apply without user_id")
        status_response_fail["error"] = "No user_id is given"
        status_response_fail["data"] = request.args
        return jsonify(status_response_fail), CODE_BAD_REQUEST
    else:
        c = cluster_handler.release_cluster(user_id)
        if not c:
            logger.warn("cluster_release failed")
            status_response_fail["error"] = "release fail for "+user_id
            status_response_fail["data"] = request.args
            return jsonify(status_response_fail), CODE_BAD_REQUEST
        else:
            return jsonify(status_response_ok), CODE_OK