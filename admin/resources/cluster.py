import logging
import os
import sys

from flask import jsonify, Blueprint, render_template
from flask import request as r
from flask.ext.paginate import Pagination


sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from common import log_handler, LOG_LEVEL, response_ok, \
    response_fail, CODE_OK, CODE_CREATED, CODE_BAD_REQUEST, \
    CONSENSUS_PLUGINS, CONSENSUS_MODES, CLUSTER_SIZES

logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
logger.addHandler(log_handler)

from modules import cluster_handler, host_handler

cluster = Blueprint('cluster', __name__)


@cluster.route('/clusters', methods=['GET'])
def clusters_show():
    logger.info("/clusters action=" + r.method)
    for k in r.args:
        logger.debug("{0}:{1}".format(k, r.args[k]))
    show_type=r.args.get("type", "active")
    col_filter = dict((key, r.args.get(key)) for key in r.args if
                      key != "col_name" and key != "page" and key !="type")
    if show_type != "released":
        col_name = r.args.get("col_name", "active")
    else:
        col_name = r.args.get("col_name", "released")

    if show_type == "inused":
        col_filter["user_id"] = {"$ne":""}

    clusters = list(cluster_handler.list(filter_data=col_filter,
                                         col_name=col_name))
    if show_type == "active":
        clusters.sort(key=lambda x: str(x["create_ts"]), reverse=True)
    elif show_type == "inused":
        clusters.sort(key=lambda x: str(x["apply_ts"]), reverse=True)
    else:
        clusters.sort(key=lambda x: str(x["release_ts"]), reverse=True)
    total_items = len(clusters)

    search = False
    q = r.args.get('q')
    if q:
        search = True
    try:
        page = int(r.args.get('page', 1))
    except ValueError:
        page = 1

    per_page = 10
    if page*per_page >= total_items:  # show ends at this page
        show_clusters = clusters[(page-1)*per_page:]
        logger.debug("last page, total={} page={},per_page={},show_items={"
                     "}".format(total_items, page, per_page, show_clusters))
    else:
        show_clusters = clusters[(page-1)*per_page:page*per_page]
        logger.debug("middle page, total={}, page={},per_page={},show_items={"
                     "}".format(total_items, page, per_page, show_clusters))

    pagination = Pagination(page=page, per_page=per_page, total=total_items,
                            search=search, record_name='clusters')

    hosts = list(host_handler.list())
    available_hosts = list(filter(
        lambda e: e["status"] == "active"
                  and len(e["clusters"]) < e["capacity"], hosts))
    return render_template("clusters.html", type=show_type, col_name=col_name,
                           items_count=total_items, items=show_clusters,
                           pagination=pagination,
                           available_hosts=available_hosts,
                           consensus_plugins=CONSENSUS_PLUGINS,
                           consensus_modes=CONSENSUS_MODES,
                           cluster_sizes=CLUSTER_SIZES)


@cluster.route('/cluster', methods=['GET', 'POST', 'DELETE'])
def cluster_api():
    logger.info("/cluster action=" + r.method)
    for k in r.args:
        logger.debug("Arg: {0}:{1}".format(k, r.args[k]))
    for k in r.form:
        logger.debug("Form: {0}:{1}".format(k, r.form[k]))
    if r.method == 'GET':
        if not r.form["id"]:
            logger.warn("cluster get without enough data")
            response_fail["error"] = "cluster GET without enough data"
            response_fail["data"] = r.form
            return jsonify(response_fail), CODE_BAD_REQUEST
        else:
            logger.debug("id=" + r.form['id'])
            result = cluster_handler.get(r.form['id'],
                                         serialization=True)
            if result:
                return jsonify(result), CODE_OK
            else:
                logger.warn("cluster not found with id=" + r.form['id'])
                response_fail["data"] = r.form
                return jsonify(response_fail), CODE_BAD_REQUEST
    elif r.method == 'POST':
        if not r.form["name"] or not r.form["host_id"] or \
                 not r.form["consensus_plugin"] or not r.form["size"]:
            logger.warn("cluster post without enough data")
            response_fail["error"] = "cluster POST without enough data"
            response_fail["data"] = r.form
            return jsonify(response_fail), CODE_BAD_REQUEST
        else:
            name, host_id, consensus_plugin, consensus_mode, size = \
                r.form['name'], r.form['host_id'], r.form['consensus_plugin'],\
                r.form['consensus_mode'] or CONSENSUS_MODES[0], int(r.form[
                    "size"])
            if consensus_plugin not in CONSENSUS_PLUGINS:
                logger.debug("Unknown consensus_plugin={}".format(
                    consensus_plugin))
                return jsonify(response_fail), CODE_BAD_REQUEST
            if consensus_plugin != CONSENSUS_PLUGINS[0] and \
                            consensus_mode not in CONSENSUS_MODES:
                logger.debug("Invalid consensus, plugin={}, mode={}".format(
                    consensus_plugin, consensus_mode))
                return jsonify(response_fail), CODE_BAD_REQUEST

            if size not in CLUSTER_SIZES:
                logger.debug("Unknown cluster size={}".format(size))
                return jsonify(response_fail), CODE_BAD_REQUEST
            if cluster_handler.create(name=name, host_id=host_id,
                                      consensus_plugin=consensus_plugin,
                                      consensus_mode=consensus_mode,
                                      size=size):
                logger.debug("cluster POST successfully")
                return jsonify(response_ok), CODE_CREATED
            else:
                logger.debug("cluster creation failed")
                response_fail["error"] = "Failed to create cluster {}".format(
                    name)
                return jsonify(response_fail), CODE_BAD_REQUEST
    elif r.method == 'DELETE':
        if not r.form["id"] or not r.form["col_name"]:
            logger.warn("cluster operation post without enough data")
            response_fail["error"] = "cluster delete without " \
                                            "enough data"
            response_fail["data"] = r.form
            return jsonify(response_fail), CODE_BAD_REQUEST
        else:
            logger.debug("cluster delete with id={0}, col_name={1}".format(
                r.form["id"], r.form["col_name"]))
            if cluster_handler.delete(id=r.form["id"],
                                      col_name=r.form["col_name"]):
                return jsonify(response_ok), CODE_OK
            else:
                logger.debug("cluster deletion failed")
                response_fail["error"] = "Failed to delete cluster {}".format(
                    r.form["id"])
                return jsonify(response_fail), CODE_BAD_REQUEST
    else:
        response_fail["error"] = "unknown operation method"
        response_fail["data"] = r.form
        return jsonify(response_fail), CODE_BAD_REQUEST


@cluster.route('/cluster_info/<cluster_id>', methods=['GET'])
def cluster_info(cluster_id):
    logger.debug("/ cluster_info/{0}?released={1} action={2}".format(
        cluster_id, r.args.get('released', '0'), r.method))
    released = (r.args.get('released', '0') != '0')
    if not released:
        return render_template("cluster_info.html",
                               item=cluster_handler.get(
                                   cluster_id, serialization=True),
                               consensus_plugins=CONSENSUS_PLUGINS), CODE_OK
    else:
        return render_template("cluster_info.html",
                               item=cluster_handler.get(
            cluster_id, serialization=True, col_name="released"),
                               consensus_plugins=CONSENSUS_PLUGINS), CODE_OK