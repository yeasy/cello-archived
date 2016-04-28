import logging
import os
import sys

from flask import jsonify, Blueprint, request, render_template

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from common import log_handler, status_response_ok, status_response_fail

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(log_handler)

from modules import cluster_handler

cluster = Blueprint('cluster', __name__)


@cluster.route('/clusters', methods=['GET'])
def clusters_show():
    logger.info("/clusters action=" + request.method)
    for k in request.args:
        logger.debug("{0}:{1}".format(k, request.args[k]))
    filter = dict((key, request.args.get(key)) for key in request.args)

    return render_template("clusters.html", items=cluster_handler.list(filter))


@cluster.route('/clusters_released', methods=['GET'])
def clusters_released_show():
    logger.info("/cluster_released action=" + request.method)
    for k in request.args:
        logger.debug("{0}:{1}".format(k, request.args[k]))
    filter = dict((key, request.args.get(key)) for key in request.args)

    return render_template("clusters_released.html",
                           items=cluster_handler.list(filter_data=filter,
                                                      released=True))


@cluster.route('/cluster', methods=['GET', 'POST', 'DELETE'])
def cluster_operation():
    logger.info("/cluster action=" + request.method)
    if request.method == 'GET':
        if "id" not in request.form:
            logger.warn("cluster get without enough data")
            status_response_fail["error"] = "cluster GET without " \
                                            "enough data"
            status_response_fail["data"] = request.form
            return jsonify(status_response_fail), 400
        else:
            logger.debug("id=" + request.form['id'])
            result = cluster_handler.get(request.form['id'],
                                         serialization=True)
            if result:
                return jsonify(result), 200
            else:
                logger.warn("cluster not found with id=" + id)
                status_response_fail["data"] = request.form
                return jsonify(status_response_fail), 400
    elif request.method == 'POST':
        if "name" not in request.form or "daemon_url" not in request.form:
            logger.warn("cluster post without enough data")
            status_response_fail["error"] = "cluster POST without enough data"
            status_response_fail["data"] = request.form
            return jsonify(status_response_fail), 400
        else:
            logger.debug("name=" + request.form['name'])
            logger.debug("daemon_url=" + request.form['daemon_url'])
            if cluster_handler.create(name=request.form['name'],
                                      daemon_url=request.form['daemon_url']):
                logger.debug("cluster POST successfully")
                return jsonify(status_response_ok), 200
            else:
                logger.debug("cluster POST failed")
                return jsonify(status_response_fail), 400
    elif request.method == 'DELETE':
        if "id" not in request.form or not request.form["id"]:
            logger.warn("cluster operation post without enough data")
            status_response_fail["error"] = "cluster delete without " \
                                            "enough data"
            status_response_fail["data"] = request.form
            return jsonify(status_response_fail), 400
        else:
            logger.debug(request.form["id"])
            logger.debug("cluster delete with id=" + request.form["id"])
            if cluster_handler.delete(id=request.form["id"]):
                return jsonify(status_response_ok), 200
            else:
                return jsonify(status_response_fail), 400
    else:
        status_response_fail["error"] = "unknown operation method"
        status_response_fail["data"] = request.form
        return jsonify(status_response_fail), 400


@cluster.route('/cluster_info/<cluster_id>', methods=['GET'])
def show(cluster_id):
    released = (request.args.get('released', 0) != 0)
    logger.debug("/ cluster_info/{0}?released={1} action={2}".format(
        cluster_id, request.args.get('released'), request.method))
    return render_template("cluster.html", cluster=cluster_handler.get(
        cluster_id, serialization=True, released=released)), 200
