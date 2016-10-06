import logging
import os
import sys

from flask import jsonify, Blueprint, render_template
from flask import request as r

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from common import log_handler, LOG_LEVEL, response_ok, \
    response_fail, CODE_OK, CODE_CREATED, CODE_BAD_REQUEST, \
    HOST_TYPES, LOG_TYPES, request_debug, request_get, LOGGING_LEVEL_CLUSTERS
from modules import host_handler

logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
logger.addHandler(log_handler)


host = Blueprint('host', __name__)


@host.route('/hosts', methods=['GET'])
def hosts_show():
    logger.info("/hosts method=" + r.method)
    request_debug(r, logger)
    # col_filter = dict((key, r.args.get(key)) for key in r.args)
    # items = list(host_handler.list(filter_data=col_filter))
    # items.sort(key=lambda x: str(x["name"]), reverse=True)
    # logger.debug(items)

    return render_template("hosts.html",
                           host_types=HOST_TYPES,
                           log_types=LOG_TYPES,
                           log_levels=LOGGING_LEVEL_CLUSTERS,
                           )


@host.route('/hosts_list', methods=['GET'])
def hosts_list():
    logger.info("/hosts_list method=" + r.method)
    request_debug(r, logger)
    col_filter = dict((key, r.args.get(key)) for key in r.args)
    items_dict = {}
    items = list(host_handler.list(filter_data=col_filter))
    items.sort(key=lambda x: str(x["name"]), reverse=True)
    logger.debug(items)
    for i in items:
        items_dict.update({
            i.get("id"): i
        })

    return jsonify({"hosts": items_dict}), CODE_OK


@host.route('/host', methods=['GET', 'POST', 'PUT', 'DELETE'])
def host_api():
    logger.debug("hightall method={}".format(r.method))
    request_debug(r, logger)
    if r.method == 'GET':
        if "id" not in r.args and "id" not in r.form:
            logger.warn("host get without enough data")
            response_fail["error"] = "host GET without enough data"
            response_fail["data"] = r.form
            return jsonify(response_fail), CODE_BAD_REQUEST
        else:
            host_id = request_get(r, "id")
            result = host_handler.get_by_id(host_id)
            if result:
                return jsonify(result), CODE_OK
            else:
                logger.warn("host not found with id=" + host_id)
                response_fail["data"] = r.form
                return jsonify(response_fail), CODE_BAD_REQUEST
    elif r.method == 'POST':
        name, daemon_url, capacity, log_type, log_server, log_level = \
            r.form['name'], r.form['daemon_url'], r.form['capacity'], \
            r.form['log_type'], r.form['log_server'], r.form['log_level']

        if "autofill" in r.form and r.form["autofill"] == "on":
            autofill = "true"
        else:
            autofill = "false"

        if "schedulable" in r.form and r.form["schedulable"] == "on":
            schedulable = "true"
        else:
            schedulable = "false"

        logger.debug("name={}, daemon_url={}, capacity={}"
                     "fillup={}, schedulable={}, log={}/{}".
                     format(name, daemon_url, capacity, autofill, schedulable,
                            log_type, log_server))
        if not name or not daemon_url or not capacity or not log_type:
            logger.warn("host post without enough data")
            response_fail["error"] = "host POST without enough data"
            response_fail["data"] = r.form
            return jsonify(response_fail), CODE_BAD_REQUEST
        else:
            result = host_handler.create(name=name, daemon_url=daemon_url,
                                         capacity=int(capacity),
                                         autofill=autofill,
                                         schedulable=schedulable,
                                         log_level=log_level,
                                         log_type=log_type,
                                         log_server=log_server)
            if result:
                logger.debug("host creation successfully")
                response_ok.update({"data": {result.get("id"): result}})
                return jsonify(response_ok), CODE_CREATED
            else:
                logger.debug("host creation failed")
                response_fail["error"] = "Failed to create host {}".format(
                    r.form["name"])
                return jsonify(response_fail), CODE_BAD_REQUEST
    elif r.method == 'PUT':
        if "id" not in r.form:
            logger.warn("host put without enough data")
            response_fail["error"] = "host PUT without enough data"
            response_fail["data"] = r.form
            return jsonify(response_fail), CODE_BAD_REQUEST
        else:
            id, d = r.form["id"], {}
            for k in r.form:
                if k != "id":
                    d[k] = r.form.get(k)
            result = host_handler.update(id, d)
            if result:
                logger.debug("host PUT successfully")
                response_ok.update({
                    "data": result,
                    "host_id": result.get("id")
                })
                return jsonify(response_ok), CODE_OK
            else:
                logger.debug("host PUT failed")
                response_fail["error"] = "Failed to update host {}".format(
                    result.get("name"))
                return jsonify(response_fail), CODE_BAD_REQUEST
    elif r.method == 'DELETE':
        if "id" not in r.form or not r.form["id"]:
            logger.warn("host operation post without enough data")
            response_fail["error"] = "host delete without enough data"
            response_fail["data"] = r.form
            return jsonify(response_fail), CODE_BAD_REQUEST
        else:
            logger.debug("host delete with id={0}".format(r.form["id"]))
            if host_handler.delete(id=r.form["id"]):
                return jsonify(response_ok), CODE_OK
            else:
                response_fail["error"] = "Failed to delete host {}".format(
                    r.form["id"])
                return jsonify(response_fail), CODE_BAD_REQUEST
    else:
        response_fail["error"] = "unknown operation method"
        response_fail["data"] = r.form
        return jsonify(response_fail), CODE_BAD_REQUEST


@host.route('/host_info/<host_id>', methods=['GET'])
def host_info(host_id):
    logger.debug("/ host_info/{0} method={1}".format(host_id, r.method))
    return render_template("host_info.html", item=host_handler.get_by_id(
        host_id)), CODE_OK


@host.route('/host_action', methods=['POST'])
def host_action():
    logger.info("/host_action, method=" + r.method)
    request_debug(r, logger)

    host_id, action = r.form['id'], r.form['action']
    if not host_id or not action:
        logger.warn("host post without enough data")
        response_fail["error"] = "host POST without enough data"
        response_fail["data"] = r.form
        return jsonify(response_fail), CODE_BAD_REQUEST
    else:
        if action == "fillup":
            if host_handler.fillup(host_id):
                logger.debug("fillup successfully")
                return jsonify(response_ok), CODE_OK
            else:
                response_fail["data"] = r.form
                response_fail["error"] = "Failed to fillup the host."
                return jsonify(response_fail), CODE_BAD_REQUEST
        elif action == "clean":
            if host_handler.clean(host_id):
                logger.debug("clean successfully")
                return jsonify(response_ok), CODE_OK
            else:
                response_fail["data"] = r.form
                response_fail["error"] = "Failed to clean the host."
                return jsonify(response_fail), CODE_BAD_REQUEST
        elif action == "reset":
            if host_handler.reset(host_id):
                logger.debug("reset successfully")
                return jsonify(response_ok), CODE_OK
            else:
                response_fail["data"] = r.form
                response_fail["error"] = "Failed to reset the host."
                return jsonify(response_fail), CODE_BAD_REQUEST

    logger.warn("unknown host action={}".format(action))
    response_fail["error"] = "unknown operation method"
    response_fail["data"] = r.form
    return jsonify(response_fail), CODE_BAD_REQUEST
