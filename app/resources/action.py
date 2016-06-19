from flask import Blueprint, request, jsonify, make_response

import logging

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from common import log_handler, LOG_LEVEL, APP_API_VERSION, \
    response_ok, response_fail, CODE_OK, CODE_CREATED, CODE_BAD_REQUEST, \
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
        response_fail["error"] = "No user_id is given"
        response_fail["data"] = request.args
        return jsonify(response_fail), CODE_BAD_REQUEST
    else:
        c = cluster_handler.apply_cluster(user_id=user_id,
                                          consensus_type=consensus_type)
        if not c:
            logger.warn("cluster_apply failed")
            response_fail["error"] = "No available res for " + user_id
            response_fail["data"] = request.args
            return jsonify(response_fail), CODE_BAD_REQUEST
        else:
            response_ok["data"] = c
            return jsonify(response_ok), CODE_OK


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
        logger.warn("cluster_release without user_id")
        response_fail["error"] = "No user_id in release"
        response_fail["data"] = request.args
        return make_response(jsonify(response_fail), CODE_BAD_REQUEST)
    else:
        result = cluster_handler.release_cluster(user_id)
        if not result:
            logger.warn("cluster_release failed")
            response_fail["error"] = "release fail for " + user_id
            response_fail["data"] = request.args
            return jsonify(response_fail), CODE_BAD_REQUEST
        else:
            return jsonify(response_ok), CODE_OK