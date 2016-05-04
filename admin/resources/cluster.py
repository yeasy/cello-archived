import logging
import os
import sys

from flask import jsonify, Blueprint, request, render_template

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from common import log_handler, LOG_LEVEL, status_response_ok, \
    status_response_fail, CODE_OK, CODE_CREATED, CODE_BAD_REQUEST, \
    CODE_NO_CONTENT

logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
logger.addHandler(log_handler)

from modules import cluster_handler

cluster = Blueprint('cluster', __name__)


@cluster.route('/clusters', methods=['GET'])
def clusters_show():
    logger.info("/clusters action=" + request.method)
    for k in request.args:
        logger.debug("{0}:{1}".format(k, request.args[k]))
    col_filter = dict((key, request.args.get(key)) for key in request.args if
                  key != "col_name")
    col_name = request.args.get("col_name", "active")
    items = list(cluster_handler.list(filter_data=col_filter,
                                      collection=col_name))

    return render_template("clusters.html", col_name=col_name,
                           items_count=len(items), items=items)
    #return render_template("test.html")


@cluster.route('/cluster', methods=['GET', 'POST', 'DELETE'])
def cluster_api():
    logger.info("/cluster action=" + request.method)
    for k in request.args:
        logger.debug("Arg: {0}:{1}".format(k, request.args[k]))
    for k in request.form:
        logger.debug("Form: {0}:{1}".format(k, request.form[k]))
    if request.method == 'GET':
        if "id" not in request.form:
            logger.warn("cluster get without enough data")
            status_response_fail["error"] = "cluster GET without " \
                                            "enough data"
            status_response_fail["data"] = request.form
            return jsonify(status_response_fail), CODE_BAD_REQUEST
        else:
            logger.debug("id=" + request.form['id'])
            result = cluster_handler.get(request.form['id'],
                                         serialization=True)
            if result:
                return jsonify(result), CODE_OK
            else:
                logger.warn("cluster not found with id=" + id)
                status_response_fail["data"] = request.form
                return jsonify(status_response_fail), CODE_BAD_REQUEST
    elif request.method == 'POST':
        if "name" not in request.form or "host_id" not in request.form:
            logger.warn("cluster post without enough data")
            status_response_fail["error"] = "cluster POST without enough data"
            status_response_fail["data"] = request.form
            return jsonify(status_response_fail), CODE_BAD_REQUEST
        else:
            name, host_id = request.form['name'], request.form['host_id']
            if cluster_handler.create(name, host_id):
                logger.debug("cluster POST successfully")
                return jsonify(status_response_ok), CODE_CREATED
            else:
                logger.debug("cluster POST failed")
                return jsonify(status_response_fail), CODE_BAD_REQUEST
    elif request.method == 'DELETE':
        if "id" not in request.form or "col_name" not in request.form or not \
                request.form["id"] or not request.form["col_name"]:
            logger.warn("cluster operation post without enough data")
            status_response_fail["error"] = "cluster delete without " \
                                            "enough data"
            status_response_fail["data"] = request.form
            return jsonify(status_response_fail), CODE_BAD_REQUEST
        else:
            logger.debug("cluster delete with id={0}, col_name={1}".format(
                request.form["id"], request.form["col_name"]))
            if cluster_handler.delete(id=request.form["id"],
                                      col_name=request.form["col_name"]):
                return jsonify(status_response_ok), CODE_NO_CONTENT
            else:
                return jsonify(status_response_fail), CODE_BAD_REQUEST
    else:
        status_response_fail["error"] = "unknown operation method"
        status_response_fail["data"] = request.form
        return jsonify(status_response_fail), CODE_BAD_REQUEST


@cluster.route('/cluster_info/<cluster_id>', methods=['GET'])
def cluster_info(cluster_id):
    logger.debug("/ cluster_info/{0}?released={1} action={2}".format(
        cluster_id, request.args.get('released', 0), request.method))
    released = (request.args.get('released', 0) != 0)
    if not released:
        return render_template("cluster_info.html", item=cluster_handler.get(
            cluster_id, serialization=True)), CODE_OK
    else:
        return render_template("cluster_info.html", item=cluster_handler.get(
            cluster_id, serialization=True, collection="released")), CODE_OK