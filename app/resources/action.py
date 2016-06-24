from flask import Blueprint, jsonify, make_response

from flask import request as r

import logging

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from common import log_handler, LOG_LEVEL, \
    response_ok, response_fail, CODE_OK, CODE_BAD_REQUEST, \
    CONSENSUS_PLUGINS, CONSENSUS_MODES, CLUSTER_SIZES

from modules import cluster_handler
logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
logger.addHandler(log_handler)

action_v1 = Blueprint('action_v1', __name__, url_prefix='/{}'.format("v1"))
action_v2 = Blueprint('action_v2', __name__, url_prefix='/{}'.format("v2"))


def debug_request(request):
    for k in r.args:
        logger.debug("Arg: {0}:{1}".format(k, r.args[k]))
    for k in request.form:
        logger.debug("Form: {0}:{1}".format(k, request.form[k]))


@action_v1.route('/cluster_apply', methods=['GET'])
@action_v2.route('/cluster_apply', methods=['POST'])
def cluster_apply():
    """
    Return a Cluster json body.
    """
    debug_request(r)
    logger.debug(r.form.get("hi"))
    logger.debug(r.args.get("hi"))
    user_id = r.form.get("consensus_type") or r.args.get("user_id", "")
    if not user_id:
        logger.warn("cluster_apply without user_id")
        response_fail["error"] = "No user_id is given"
        response_fail["data"] = r.args
        return jsonify(response_fail), CODE_BAD_REQUEST
    consensus_type = r.form.get("consensus_type") or \
                     r.args.get("consensus_type", CONSENSUS_PLUGINS[0])

    consensus_plugin = r.form.get("consensus_plugin") or \
                       r.args.get("consensus_plugin", CONSENSUS_PLUGINS[0])
    consensus_mode = r.form.get("consensus_mode") or \
                     r.args.get("consensus_mode", CONSENSUS_MODES[0])
    cluster_size = r.form.get("size") or \
                   r.args.get("size", CLUSTER_SIZES[0])
    c = cluster_handler.apply_cluster(user_id=user_id,
                                      consensus_plugin=consensus_plugin,
                                      consensus_mode=consensus_mode,
                                      size=cluster_size)
    if not c:
        logger.warn("cluster_apply failed")
        response_fail["error"] = "No available res for " + user_id
        response_fail["data"] = r.args
        return jsonify(response_fail), CODE_BAD_REQUEST
    else:
        response_ok["data"] = c
        return jsonify(response_ok), CODE_OK


@action_v1.route('/cluster_release', methods=['GET'])
@action_v2.route('/cluster_release', methods=['POST'])
def cluster_release():
    """
    Return status.
    """
    debug_request(r)
    user_id = r.form.get("user_id", "") or r.args.get("user_id", "")
    cluster_id = r.form.get("cluster_id", "") or r.args.get("cluster_id", "")
    if not user_id and not cluster_id:
        logger.warn("cluster_release without id")
        response_fail["error"] = "No id in release"
        response_fail["data"] = r.args
        return make_response(jsonify(response_fail), CODE_BAD_REQUEST)
    else:
        if cluster_id:
            result = cluster_handler.release_cluster(cluster_id=cluster_id)
        elif user_id:
            result = cluster_handler.release_cluster_for_user(user_id=user_id)
        if not result:
            logger.warn("cluster_release failed user_id={} cluster_id={"
                        "}".format(user_id, cluster_id))
            response_fail["error"] = "release fail"
            response_fail["data"] = r.args
            return jsonify(response_fail), CODE_BAD_REQUEST
        else:
            return jsonify(response_ok), CODE_OK