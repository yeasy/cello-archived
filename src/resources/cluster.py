import logging
import os
import sys

from flask import jsonify, Blueprint, render_template
from flask import request as r

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from common import log_handler, LOG_LEVEL, \
    request_get, make_ok_response, make_fail_response, \
    request_debug, \
    CODE_OK, CODE_CREATED, CODE_BAD_REQUEST, CODE_NOT_FOUND, \
    CONSENSUS_PLUGINS, CONSENSUS_MODES, CLUSTER_SIZES
from modules import cluster_handler, host_handler

logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
logger.addHandler(log_handler)


bp_cluster_api = Blueprint('bp_cluster_api', __name__,
                           url_prefix='/{}'.format("api"))

front_rest_v2 = Blueprint('front_rest_v2', __name__,
                          url_prefix='/{}'.format("v2"))


def cluster_start(r):
    """Start a cluster which should be in stopped status currently.

    :param r:
    :return:
    """
    cluster_id = request_get(r, "cluster_id")
    if not cluster_id:
        logger.warning("No cluster_id is given")
        return make_fail_response("No cluster_id is given")
    if cluster_handler.start(cluster_id):
        return make_ok_response(), CODE_OK

    return make_fail_response("cluster start failed")


def cluster_restart(r):
    """Start a cluster which should be in stopped status currently.

    :param r:
    :return:
    """
    cluster_id = request_get(r, "cluster_id")
    if not cluster_id:
        logger.warning("No cluster_id is given")
        return make_fail_response("No cluster_id is given")
    if cluster_handler.restart(cluster_id):
        return make_ok_response(), CODE_OK

    return make_fail_response("cluster restart failed")


def cluster_stop(r):
    """Stop a cluster which should be in running status currently.

    :param r:
    :return:
    """
    cluster_id = request_get(r, "cluster_id")
    if not cluster_id:
        logger.warning("No cluster_id is given")
        return make_fail_response("No cluster_id is given")
    if cluster_handler.stop(cluster_id):
        return make_ok_response(), CODE_OK

    return make_fail_response("cluster stop failed")


def cluster_apply(r):
    """Apply a cluster.

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
        return make_ok_response(data=c), CODE_OK


def cluster_release(r):
    """Release a cluster which should be in used status currently.

    :param r:
    :return:
    """
    cluster_id = request_get(r, "cluster_id")
    if not cluster_id:
        logger.warning("No cluster_id is given")
        return make_fail_response("No cluster_id is given")
    if cluster_handler.release_cluster(cluster_id):
        return make_ok_response(), CODE_OK

    return make_fail_response("cluster release failed")


@front_rest_v2.route('/cluster_op', methods=['GET', 'POST'])
@bp_cluster_api.route('/cluster_op', methods=['GET', 'POST'])
def cluster_actions():
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
        return cluster_apply(r)
    elif action == "release":
        return cluster_release(r)
    elif action == "start":
        return cluster_start(r)
    elif action == "stop":
        return cluster_stop(r)
    elif action == "restart":
        return cluster_restart(r)
    else:
        return make_fail_response("Unknown action type")


@bp_cluster_api.route('/cluster/<cluster_id>', methods=['GET'])
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
        return make_fail_response(error=error_msg, data=r.form,
                                  code=CODE_NOT_FOUND), \
               CODE_NOT_FOUND


@bp_cluster_api.route('/cluster', methods=['POST'])
def cluster_create():
    """ Handle cluster related operations.

    GET: Get a json object of the cluster, e.g., /cluster/xxxx
    POST: Do some action on the cluster
    DELETE: Delete a cluster

    :return:
    """
    logger.info("/cluster action=" + r.method)
    request_debug(r, logger)
    if not r.form["name"] or not r.form["host_id"] or not \
            r.form["consensus_plugin"] or not r.form["size"]:
        error_msg = "cluster post without enough data"
        logger.warning(error_msg)
        return make_fail_response(error=error_msg, data=r.form), \
               CODE_BAD_REQUEST
    else:
        name, host_id, consensus_plugin, consensus_mode, size = \
            r.form['name'], r.form['host_id'], r.form['consensus_plugin'],\
            r.form['consensus_mode'] or CONSENSUS_MODES[0], int(r.form[
                "size"])
        if consensus_plugin not in CONSENSUS_PLUGINS:
            logger.debug("Unknown consensus_plugin={}".format(
                consensus_plugin))
            return make_fail_response(), CODE_BAD_REQUEST
        if consensus_plugin != CONSENSUS_PLUGINS[0] and consensus_mode \
                not in CONSENSUS_MODES:
            logger.debug("Invalid consensus, plugin={}, mode={}".format(
                consensus_plugin, consensus_mode))
            return make_fail_response(), CODE_BAD_REQUEST

        if size not in CLUSTER_SIZES:
            logger.debug("Unknown cluster size={}".format(size))
            return make_fail_response(), CODE_BAD_REQUEST
        if cluster_handler.create(name=name, host_id=host_id,
                                  consensus_plugin=consensus_plugin,
                                  consensus_mode=consensus_mode,
                                  size=size):
            logger.debug("cluster POST successfully")
            return make_ok_response(), CODE_CREATED
        else:
            logger.debug("cluster creation failed")
            return make_fail_response(
                error="Failed to create cluster {}".format(name)), \
                   CODE_BAD_REQUEST


@bp_cluster_api.route('/cluster', methods=['DELETE'])
def cluster_delete():
    """ Handle cluster related operations.

    GET: Get a json object of the cluster, e.g., /cluster/xxxx
    POST: Do some action on the cluster
    DELETE: Delete a cluster

    :return:
    """
    logger.info("/cluster action=" + r.method)
    request_debug(r, logger)
    if not r.form["id"] or not r.form["col_name"]:
        error_msg = "cluster operation post without enough data"
        logger.warning(error_msg)
        return make_fail_response(error=error_msg, data=r.form), CODE_BAD_REQUEST
    else:
        logger.debug("cluster delete with id={0}, col_name={1}".format(
            r.form["id"], r.form["col_name"]))
        if r.form["col_name"] == "active":
            result = cluster_handler.delete(id=r.form["id"])
        else:
            result = cluster_handler.delete_released(id=r.form["id"])
        if result:
            return make_ok_response(), CODE_OK
        else:
            error_msg = "Failed to delete cluster {}".format(r.form["id"])
            logger.warning(error_msg)
            return make_fail_response(error=error_msg), CODE_BAD_REQUEST


@bp_cluster_api.route('/clusters', methods=['GET', 'POST'])
@front_rest_v2.route('/clusters', methods=['GET', 'POST'])
def cluster_list():
    """
    Return list of the clusters.
    """
    request_debug(r, logger)
    json_body = r.get_json(force=True, silent=True) or {}
    result = cluster_handler.list(filter_data=json_body)
    return make_ok_response(data=result), CODE_OK


bp_cluster_view = Blueprint('bp_cluster_view', __name__,
                            url_prefix='/{}'.format("view"))


# Return a web page with cluster info
@bp_cluster_view.route('/cluster/<cluster_id>', methods=['GET'])
def cluster_info_show(cluster_id):
    logger.debug("/ cluster_info/{}?released={} action={}".format(
        cluster_id, r.args.get('released', '0'), r.method))
    released = (r.args.get('released', '0') != '0')
    if not released:
        return render_template("cluster_info.html",
                               item=cluster_handler.get_by_id(cluster_id),
                               consensus_plugins=CONSENSUS_PLUGINS), CODE_OK
    else:
        return render_template("cluster_info.html",
                               item=cluster_handler.get_by_id(
                                   cluster_id, col_name="released"),
                               consensus_plugins=CONSENSUS_PLUGINS), CODE_OK


# Return a web page with clusters
@bp_cluster_view.route('/clusters', methods=['GET'])
def clusters_show():
    request_debug(r, logger)
    show_type = r.args.get("type", "active")
    col_filter = dict((key, r.args.get(key)) for key in r.args if
                      key != "col_name" and key != "page" and key != "type")
    if show_type != "released":
        col_name = r.args.get("col_name", "active")
    else:
        col_name = r.args.get("col_name", "released")

    if show_type == "inused":
        col_filter["user_id"] = {"$ne": ""}

    clusters = list(cluster_handler.list(filter_data=col_filter,
                                         col_name=col_name))
    if show_type == "active":
        clusters.sort(key=lambda x: str(x["create_ts"]), reverse=True)
    elif show_type == "inused":
        clusters.sort(key=lambda x: str(x["apply_ts"]), reverse=True)
    else:
        clusters.sort(key=lambda x: str(x["release_ts"]), reverse=True)
    total_items = len(clusters)

    hosts = list(host_handler.list())
    hosts_avail = list(filter(lambda e: e["status"] == "active" and len(
        e["clusters"]) < e["capacity"], hosts))
    return render_template("clusters.html", type=show_type, col_name=col_name,
                           items_count=total_items, items=clusters,
                           hosts_available=hosts_avail,
                           consensus_plugins=CONSENSUS_PLUGINS,
                           consensus_modes=CONSENSUS_MODES,
                           cluster_sizes=CLUSTER_SIZES)


# will deprecate
@front_rest_v2.route('/cluster_apply', methods=['GET', 'POST'])
def cluster_apply_dep():
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
            error_msg = "Invalid cluster_size"
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
@front_rest_v2.route('/cluster_release', methods=['GET', 'POST'])
def cluster_release_dep():
    """
    Return status.
    """
    request_debug(r, logger)
    user_id = request_get(r, "user_id")
    cluster_id = request_get(r, "cluster_id")
    if not user_id and not cluster_id:
        error_msg = "cluster_release without id"
        logger.warning(error_msg)
        return make_fail_response(error=error_msg, data=r.args), CODE_BAD_REQUEST
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
            return make_fail_response(error=error_msg, data=data), \
                   CODE_BAD_REQUEST
        else:
            return make_ok_response(), CODE_OK
