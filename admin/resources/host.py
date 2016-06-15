import logging
import os
import sys

from flask import jsonify, Blueprint, render_template
from flask import request as r

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from common import log_handler, LOG_LEVEL, status_response_ok, \
    status_response_fail, CODE_OK, CODE_CREATED, CODE_BAD_REQUEST, \
    CODE_NO_CONTENT, HOST_TYPES

logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
logger.addHandler(log_handler)

from modules import host_handler

host = Blueprint('host', __name__)


@host.route('/hosts', methods=['GET'])
def hosts_show():
    logger.info("/hosts action=" + r.method)
    for k in r.args:
        logger.debug("{0}:{1}".format(k, r.args[k]))
    col_filter = dict((key, r.args.get(key)) for key in r.args)
    items = list(host_handler.list(filter_data=col_filter))

    return render_template("hosts.html", items_count=len(items),
                           items=items, host_types=HOST_TYPES)


@host.route('/host', methods=['GET', 'POST', 'PUT', 'DELETE'])
def host_api():
    logger.info("/host method=" + r.method)
    for k in r.args:
        logger.debug("Arg: {0}:{1}".format(k, r.args[k]))
    for k in r.form:
        logger.debug("Form: {0}:{1}".format(k, r.form[k]))
    if r.method == 'GET':
        if "id" not in r.args and "id" not in r.form:
            logger.warn("host get without enough data")
            status_response_fail["error"] = "host GET without " \
                                            "enough data"
            status_response_fail["data"] = r.form
            return jsonify(status_response_fail), CODE_BAD_REQUEST
        else:
            host_id = r.args.get("id") or r.form.get("id")
            logger.debug("id=" + host_id)
            result = host_handler.get(host_id, serialization=True)
            if result:
                return jsonify(result), CODE_OK
            else:
                logger.warn("host not found with id=" + host_id)
                status_response_fail["data"] = r.form
                return jsonify(status_response_fail), CODE_BAD_REQUEST
    elif r.method == 'POST':
        name, daemon_url, capacity, status = r.form['name'], r.form[
            'daemon_url'], r.form['capacity'], r.form['status']
        logger.debug("name={}, daemon_url={}, capacity={}, status={}"
                     .format( name, daemon_url, capacity, status))
        if not name or not daemon_url or not capacity or not status:
            logger.warn("host post without enough data")
            status_response_fail["error"] = "host POST without enough data"
            status_response_fail["data"] = r.form
            return jsonify(status_response_fail), CODE_BAD_REQUEST
        else:
            if host_handler.create(name, daemon_url, int(capacity), status):
                logger.debug("host POST successfully")
                return jsonify(status_response_ok), CODE_CREATED
            else:
                logger.debug("host POST failed")
                return jsonify(status_response_fail), CODE_BAD_REQUEST
    elif r.method == 'PUT':
        if "id" not in r.form:
            logger.warn("host put without enough data")
            status_response_fail["error"] = "host PUT without enough data"
            status_response_fail["data"] = r.form
            return jsonify(status_response_fail), CODE_BAD_REQUEST
        else:
            id, d = r.form["id"], {}
            for k in r.form:
                if k != "id":
                    d[k] = r.form.get(k)
            if host_handler.update(id, d):
                logger.debug("host PUT successfully")
                return jsonify(status_response_ok), CODE_CREATED
            else:
                logger.debug("host PUT failed")
                return jsonify(status_response_fail), CODE_BAD_REQUEST
    elif r.method == 'DELETE':
        if "id" not in r.form or not r.form["id"]:
            logger.warn("host operation post without enough data")
            status_response_fail["error"] = "host delete without " \
                                            "enough data"
            status_response_fail["data"] = r.form
            return jsonify(status_response_fail), CODE_BAD_REQUEST
        else:
            logger.debug("host delete with id={0}".format(r.form["id"]))
            if host_handler.delete(id=r.form["id"]):
                return jsonify(status_response_ok), CODE_NO_CONTENT
            else:
                return jsonify(status_response_fail), CODE_BAD_REQUEST
    else:
        status_response_fail["error"] = "unknown operation method"
        status_response_fail["data"] = r.form
        return jsonify(status_response_fail), CODE_BAD_REQUEST


@host.route('/host_info/<host_id>', methods=['GET'])
def host_info(host_id):
    logger.debug("/ host_info/{0} action={1}".format(host_id, r.method))
    return render_template("host_info.html", item=host_handler.get(
        host_id, serialization=True)), CODE_OK


@host.route('/host_action', methods=['POST'])
def host_action():
    logger.info("/host_action, method=" + r.method)
    for k in r.args:
        logger.debug("Arg: {0}:{1}".format(k, r.args[k]))
    for k in r.form:
        logger.debug("Form: {0}:{1}".format(k, r.form[k]))

    host_id, action = r.form['id'], r.form['action']
    logger.debug("host id={}, action={}".format(host_id, action))
    if not host_id or not action:
        logger.warn("host post without enough data")
        status_response_fail["error"] = "host POST without enough data"
        status_response_fail["data"] = r.form
        return jsonify(status_response_fail), CODE_BAD_REQUEST
    else:
        if action == "fillup":
            if host_handler.fillup(host_id):
                logger.debug("fillup successfully")
                return jsonify(status_response_ok), CODE_OK
        elif action == "clean":
            if host_handler.clean(host_id):
                logger.debug("clean successfully")
                return jsonify(status_response_ok), CODE_OK
        else:
            logger.warn("unknown host action={}".format(action))

    status_response_fail["error"] = "unknown operation method"
    status_response_fail["data"] = r.form
    return jsonify(status_response_fail), CODE_BAD_REQUEST
