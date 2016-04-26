import __future__
import os
import sys

from flask import jsonify, Blueprint, request, render_template

import logging
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from common import log_handler, status_response_ok, status_response_fail
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(log_handler)

from modules import cluster_handler

cluster = Blueprint('cluster', __name__)


@cluster.route('/clusters', methods=['GET'])
def clusters_show():
    return render_template("clusters.html", items=cluster_handler.list())


@cluster.route('/cluster', methods=['GET', 'POST', 'DELETE'])
def cluster_operation():
    logger.info("action="+request.method)
    if request.method == 'GET':  # TODO
        if "id" not in request.form:
            logger.warn("cluster get without enough data")
            status_response_fail["error"] = "cluster operation get without " \
                                            "enough data"
            status_response_fail["data"] = jsonify(request.form)
            return jsonify(status_response_fail), 400
        else:
            logger.debug("id="+request.form['id'])
            return jsonify(cluster_handler.get(request.form['id'],
                                               serialization=True)), 200
    elif request.method == 'POST':
        if "name" not in request.form or "daemon_url" not in request.form:
            logger.warn("cluster post without enough data")
            status_response_fail["error"] = "cluster operation post without enough data"
            status_response_fail["data"] = jsonify(request.form)
            return jsonify(status_response_fail), 400
        else:
            logger.debug("name="+request.form['name'])
            logger.debug("daemon_url="+request.form['daemon_url'])
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
            status_response_fail["data"] = jsonify(request.form)
            return jsonify(status_response_fail), 400
        else:
            logger.debug(request.form["id"])
            logger.debug("cluster delete with id="+request.form["id"])
            if cluster_handler.delete(id=request.form["id"]):
                return jsonify(status_response_ok), 200
            else:
                return jsonify(status_response_fail), 400
    else:
        status_response_fail["error"] = "unknown operation method"
        status_response_fail["data"] = jsonify(request.form)
        return jsonify(status_response_fail), 400


@cluster.route('/cluster_info/<cluster_id>', methods=['GET'])
def show(cluster_id):
    logger.info("action="+request.method)
    return render_template("cluster.html", cluster=cluster_handler.get(
        cluster_id, serialization=True)), 200
