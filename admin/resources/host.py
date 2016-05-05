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

from modules import host_handler

host = Blueprint('host', __name__)


@host.route('/hosts', methods=['GET'])
def hosts_show():
    logger.info("/hosts action=" + request.method)
    for k in request.args:
        logger.debug("{0}:{1}".format(k, request.args[k]))
    col_filter = dict((key, request.args.get(key)) for key in request.args)
    items = list(host_handler.list(filter_data=col_filter))

    return render_template("hosts.html", items_count=len(items), items=items)
    #return render_template("test.html")


@host.route('/host', methods=['GET', 'POST', 'PUT', 'DELETE'])
def host_api():
    logger.info("/host action=" + request.method)
    for k in request.args:
        logger.debug("Arg: {0}:{1}".format(k, request.args[k]))
    for k in request.form:
        logger.debug("Form: {0}:{1}".format(k, request.form[k]))
    if request.method == 'GET':
        if "id" not in request.args and "id" not in request.form:
            logger.warn("host get without enough data")
            status_response_fail["error"] = "host GET without " \
                                            "enough data"
            status_response_fail["data"] = request.form
            return jsonify(status_response_fail), CODE_BAD_REQUEST
        else:
            host_id = request.args.get("id") or request.form.get("id")
            logger.debug("id=" + host_id)
            result = host_handler.get(host_id, serialization=True)
            if result:
                return jsonify(result), CODE_OK
            else:
                logger.warn("host not found with id=" + host_id)
                status_response_fail["data"] = request.form
                return jsonify(status_response_fail), CODE_BAD_REQUEST
    elif request.method == 'POST':
        if "name" not in request.form or "daemon_url" not in request.form:
            logger.warn("host post without enough data")
            status_response_fail["error"] = "host POST without enough data"
            status_response_fail["data"] = request.form
            return jsonify(status_response_fail), CODE_BAD_REQUEST
        else:
            name, daemon_url, capacity = request.form['name'], request.form[
                'daemon_url'], int(request.form['capacity'])
            logger.debug("name={}, daemon_url={}, capacity={}".format(name,
                                                              daemon_url, capacity))
            if host_handler.create(name, daemon_url, capacity):
                logger.debug("host POST successfully")
                return jsonify(status_response_ok), CODE_CREATED
            else:
                logger.debug("host POST failed")
                return jsonify(status_response_fail), CODE_BAD_REQUEST
    elif request.method == 'PUT':
        if "id" not in request.form or "name" not in request.form or "capacity" not in request.form:
            logger.warn("host put without enough data")
            status_response_fail["error"] = "host PUT without enough data"
            status_response_fail["data"] = request.form
            return jsonify(status_response_fail), CODE_BAD_REQUEST
        else:
            id, name, capacity = request.form['id'], request.form['name'], \
                                 int(request.form['capacity'])
            logger.debug("id={}, name={}, capacity={}".format(id, name,
                                                              capacity))
            d = {
                "name": name,
                "capacity": capacity
            }
            if host_handler.update(id, d):
                logger.debug("host PUT successfully")
                return jsonify(status_response_ok), CODE_CREATED
            else:
                logger.debug("host PUT failed")
                return jsonify(status_response_fail), CODE_BAD_REQUEST
    elif request.method == 'DELETE':
        if "id" not in request.form or not request.form["id"]:
            logger.warn("host operation post without enough data")
            status_response_fail["error"] = "host delete without " \
                                            "enough data"
            status_response_fail["data"] = request.form
            return jsonify(status_response_fail), CODE_BAD_REQUEST
        else:
            logger.debug("host delete with id={0}".format(request.form["id"]))
            if host_handler.delete(id=request.form["id"]):
                return jsonify(status_response_ok), CODE_NO_CONTENT
            else:
                return jsonify(status_response_fail), CODE_BAD_REQUEST
    else:
        status_response_fail["error"] = "unknown operation method"
        status_response_fail["data"] = request.form
        return jsonify(status_response_fail), CODE_BAD_REQUEST


@host.route('/host_info/<host_id>', methods=['GET'])
def host_info(host_id):
    logger.debug("/ host_info/{0} action={1}".format(host_id, request.method))
    return render_template("host_info.html", item=host_handler.get(
        host_id, serialization=True)), CODE_OK