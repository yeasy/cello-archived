# This module will be deprecated soon.
from flask import Blueprint, jsonify, make_response
from flask import request as r

import logging
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from common import log_handler, LOG_LEVEL, \
    make_ok_response, make_fail_response, \
    CODE_OK, CODE_BAD_REQUEST, CODE_NOT_FOUND, \
    CONSENSUS_PLUGINS, CONSENSUS_MODES, \
    CLUSTER_SIZES, request_debug, request_get

from modules import cluster_handler
from .cluster import cluster_start, cluster_stop, cluster_restart


logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
logger.addHandler(log_handler)

front_rest_v1 = Blueprint('front_rest_v1', __name__,
                          url_prefix='/{}'.format("v1"))
front_rest_v2 = Blueprint('front_rest_v2', __name__,
                          url_prefix='/{}'.format("v2"))


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
        return make_ok_response(), CODE_OK
    elif action == "release":
        return make_ok_response(), CODE_OK
    elif action == "start":
        return cluster_start(r)
    elif action == "stop":
        return cluster_stop(r)
    elif action == "restart":
        return cluster_restart(r)
    else:
        return make_fail_response(error="Unknown action type")


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
        error_msg = "cluster_apply without user_id"
        logger.warning(error_msg)
        return make_fail_response(error=error_msg)

    allow_multiple, condition = request_get(r, "allow_multiple"), {}

    consensus_plugin = request_get(r, "consensus_plugin")
    consensus_mode = request_get(r, "consensus_mode")
    cluster_size = int(request_get(r, "size") or -1)
    if consensus_plugin:
        if consensus_plugin not in CONSENSUS_PLUGINS:
            error_msg = "Invalid consensus_plugin"
            logger.warning(error_msg)
            return make_fail_response(error=error_msg)
        else:
            condition["consensus_plugin"] = consensus_plugin

    if consensus_mode:
        if consensus_mode not in CONSENSUS_MODES:
            error_msg = "Invalid consensus_mode"
            logger.warning(error_msg)
            return make_fail_response(error=error_msg)
        else:
            condition["consensus_mode"] = consensus_mode

    if cluster_size >= 0:
        if cluster_size not in CLUSTER_SIZES:
            error_msg = "Invalid cluster size"
            logger.warning(error_msg)
            return make_fail_response(error=error_msg)
        else:
            condition["size"] = cluster_size

    logger.debug("condition={}".format(condition))
    c = cluster_handler.apply_cluster(user_id=user_id, condition=condition,
                                      allow_multiple=allow_multiple)
    if not c:
        error_msg = "No available res for {}".format(user_id)
        logger.warning(error_msg)
        return make_fail_response(error=error_msg)
    else:
        return make_ok_response(data=c), CODE_OK


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
        error_msg = "No id in release"
        logger.warning(error_msg)
        return make_fail_response(error=error_msg,
                                  data=r.args), CODE_BAD_REQUEST
    else:
        result = None
        if cluster_id:
            result = cluster_handler.release_cluster(cluster_id=cluster_id)
        elif user_id:
            result = cluster_handler.release_cluster_for_user(user_id=user_id)
        if not result:
            error_msg = "cluster_release failed user_id={} cluster_id={}". \
                format(user_id, cluster_id)
            logger.warning(error_msg)
            data = {
                "user_id": user_id,
                "cluster_id": cluster_id,
            }
            return make_fail_response(error=error_msg,
                                      data=data), CODE_BAD_REQUEST
        else:
            return make_ok_response(), CODE_OK


@front_rest_v2.route('/clusters', methods=['POST'])
def cluster_list():
    """
    Return list of the clusters.
    """
    request_debug(r, logger)
    json_body = r.get_json(force=True, silent=True)
    result = cluster_handler.list(filter_data=json_body)
    return make_ok_response(data=result), CODE_OK


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
        return make_ok_response(data=result), CODE_OK
    else:
        error_msg = "cluster not found with id=" + cluster_id
        logger.warning(error_msg)
        return make_fail_response(error=error_msg,
                                  data=r.form), CODE_NOT_FOUND
