from flask import Blueprint, jsonify, make_response

from flask import request as r

import logging

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from common import log_handler, LOG_LEVEL, response_ok, response_fail, \
    CODE_OK, CODE_BAD_REQUEST, CODE_NOT_FOUND, \
    CONSENSUS_PLUGINS, CONSENSUS_MODES, \
    CLUSTER_SIZES, request_debug, request_get, request_json_body

from modules import cluster_handler
from .cluster import cluster_start, cluster_stop, cluster_restart, \
    make_fail_response


logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
logger.addHandler(log_handler)

front_rest_v1 = Blueprint('front_rest_v1', __name__, url_prefix='/{}'.format("v1"))
front_rest_v2 = Blueprint('front_rest_v2', __name__, url_prefix='/{}'.format("v2"))


# REST API to operate a cluster
@front_rest_v2.route('/cluster_op', methods=['GET', 'POST'])
def cluster_op():
    """ Issue some operations on the cluster.
    e.g., /cluster_op?action=apply&user_id=xxx will apply a cluster for user

    apply:
    release:
    start:
    stop:
    restart:

    Return a json obj.
    """
    request_debug(r, logger)
    action = request_get(r, "action")
    logger.info("cluster_op with action={}".format(action))
    if action == "apply":
        return jsonify(response_ok), CODE_OK
    elif action == "release":
        return jsonify(response_ok), CODE_OK
    elif action == "start":
        return cluster_start(r)
    elif action == "stop":
        return cluster_stop(r)
    elif action == "restart":
        return cluster_restart(r)
    else:
        return make_fail_response("Unknown action type")


# will deprecate
@front_rest_v1.route('/cluster_apply', methods=['GET'])
@front_rest_v2.route('/cluster_apply', methods=['GET', 'POST'])
def cluster_apply():
    """
    Return a Cluster json body.
    """
    request_debug(r, logger)

    user_id = request_get(r, "user_id")
    if not user_id:
        logger.warning("cluster_apply without user_id")
        return make_fail_response("cluster_apply without user_id")

    allow_multiple, condition = request_get(r, "allow_multiple"), {}

    consensus_plugin = request_get(r, "consensus_plugin")
    consensus_mode = request_get(r, "consensus_mode")
    cluster_size = int(request_get(r, "size") or -1)
    if consensus_plugin:
        if consensus_plugin not in CONSENSUS_PLUGINS:
            logger.warning("Invalid consensus_plugin")
            return make_fail_response("Invalid consensus_plugin")
        else:
            condition["consensus_plugin"] = consensus_plugin

    if consensus_mode:
        if consensus_mode not in CONSENSUS_MODES:
            logger.warning("Invalid consensus_mode")
            return make_fail_response("Invalid consensus_mode")
        else:
            condition["consensus_mode"] = consensus_mode

    if cluster_size >= 0:
        if cluster_size not in CLUSTER_SIZES:
            logger.warning("Invalid cluster_size")
            return make_fail_response("Invalid cluster_size")
        else:
            condition["size"] = cluster_size

    logger.debug("condition={}".format(condition))
    c = cluster_handler.apply_cluster(user_id=user_id, condition=condition,
                                      allow_multiple=allow_multiple)
    if not c:
        logger.warning("cluster_apply failed")
        return make_fail_response("No available res for {}".format(user_id))
    else:
        response_ok["data"] = c
        return jsonify(response_ok), CODE_OK


# will deprecate
@front_rest_v1.route('/cluster_release', methods=['GET'])
@front_rest_v2.route('/cluster_release', methods=['GET', 'POST'])
def cluster_release():
    """
    Return status.
    """
    request_debug(r, logger)
    user_id = request_get(r, "user_id")
    cluster_id = request_get(r, "cluster_id")
    if not user_id and not cluster_id:
        logger.warning("cluster_release without id")
        response_fail["error"] = "No id in release"
        response_fail["data"] = r.args
        return make_response(jsonify(response_fail), CODE_BAD_REQUEST)
    else:
        result = None
        if cluster_id:
            result = cluster_handler.release_cluster(cluster_id=cluster_id)
        elif user_id:
            result = cluster_handler.release_cluster_for_user(user_id=user_id)
        if not result:
            logger.warning("cluster_release failed user_id={} cluster_id={}".
                           format(user_id, cluster_id))
            response_fail["error"] = "release fail"
            response_fail["data"] = {
                "user_id": user_id,
                "cluster_id": cluster_id,
            }
            return jsonify(response_fail), CODE_BAD_REQUEST
        else:
            return jsonify(response_ok), CODE_OK


@front_rest_v2.route('/clusters', methods=['POST'])
def cluster_list():
    """
    Return list of the clusters.
    """
    request_debug(r, logger)
    json_body = r.get_json(force=True, silent=True)
    result = cluster_handler.list(filter_data=json_body)
    response_ok["data"] = result
    return jsonify(response_ok), CODE_OK


@front_rest_v2.route('/cluster/<cluster_id>', methods=['GET'])
def cluster_query(cluster_id):
    """
    Return a json obj of the cluster.
    """
    request_debug(r, logger)
    # cluster_id = request_get(r, "cluster_id")

    result = cluster_handler.get_by_id(cluster_id)
    logger.info(result)
    if result:
        response_ok['data'] = result
        return jsonify(response_ok), CODE_OK
    else:
        logger.warning("cluster not found with id=" + cluster_id)
        response_fail["data"] = r.form
        response_fail["code"] = CODE_NOT_FOUND
        return jsonify(response_fail), CODE_NOT_FOUND
