from flask import Blueprint, request, jsonify

import logging

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from common import log_handler, status_response_ok, status_response_fail
from modules import cluster_handler
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(log_handler)

action = Blueprint('action', __name__, url_prefix='/v1')


@action.route('/cluster_apply', methods=['GET'])
def cluster_apply():
    """
    Return a Cluster json body.
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
        return jsonify(status_response_fail), 400
    else:
        c = cluster_handler.apply_cluster(user_id)
        if not c:
            logger.warn("cluster_apply failed")
            status_response_fail["error"] = "No available res for "+user_id
            status_response_fail["data"] = request.args
            return jsonify(status_response_fail), 400
        else:
            return jsonify(c), 200


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
        return jsonify(status_response_fail), 400
    else:
        c = cluster_handler.release_cluster(user_id)
        if not c:
            logger.warn("cluster_release failed")
            status_response_fail["error"] = "release fail for "+user_id
            status_response_fail["data"] = request.args
            return jsonify(status_response_fail), 400
        else:
            return jsonify(status_response_ok), 200

