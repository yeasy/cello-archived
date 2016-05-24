import logging
import os
import sys

from flask import Blueprint, jsonify, render_template
from flask import request as r

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from common import log_handler, LOG_LEVEL, CONSENSUS_TYPES, HOST_TYPES, \
CODE_OK, HOST_TYPES
from version import version, version_info, author

logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
logger.addHandler(log_handler)

from modules import cluster_handler, host_handler, stat_handler

stat = Blueprint('stat', __name__)


@stat.route('/stat', methods=['GET'])
def show():
    logger.info("path={}, action={}".format(r.path, r.method))

    return render_template("stat.html")


@stat.route('/_health', methods=['GET'])
def health():
    logger.info("path={}, action={}".format(r.path, r.method))
    result = {
        'health': 'OK',
        'version': version
    }

    return jsonify(result), CODE_OK


@stat.route('/_stat', methods=['GET'])
def get():
    logger.info("path={}, action={}".format(r.path, r.method))
    for k in r.args:
        logger.debug("Arg: {0}:{1}".format(k, r.args[k]))
    for k in r.form:
        logger.debug("Form: {0}:{1}".format(k, r.form[k]))
    res = r.args.get('res')
    if res == 'hosts':
        result = stat_handler.hosts()
    elif res == 'clusters':
        result = stat_handler.clusters()
    else:
        result = {
            'example': '_stat?res=hosts'
        }

    logger.debug(result)
    return jsonify(result), CODE_OK
