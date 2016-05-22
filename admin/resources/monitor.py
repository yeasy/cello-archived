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

from modules import cluster_handler, host_handler

monitor = Blueprint('monitor', __name__)


@monitor.route('/monitor', methods=['GET'])
def show():
    logger.info("path={}, action={}".format(r.path, r.method))

    return render_template("monitor.html")


@monitor.route('/_health', methods=['GET'])
def health():
    logger.info("path={}, action={}".format(r.path, r.method))
    result = {
        'health': 'OK'
    }

    return jsonify(result), CODE_OK


@monitor.route('/_stat', methods=['GET'])
def stat():
    logger.info("path={}, action={}".format(r.path, r.method))
    res = r.args.get('res')
    result = {'data': []}
    total_hosts = list(host_handler.list())
    if res == 'hosts_status':
        hosts = list(host_handler.list())
        active_hosts = list(host_handler.list(filter_data={'status':
                                                               'active'}))
        inactive_hosts = list(host_handler.list(filter_data={'status':
                                                               'inactive'}))
        result['data'] = [
            {'name': 'active', 'y': len(active_hosts)},
            {'name':'inactive', 'y': len(inactive_hosts)}
        ]
    elif res == 'hosts_type':
        for host_type in HOST_TYPES:
            hosts = list(host_handler.list(filter_data={'type': host_type}))
            result['data'].append({
                'name': host_type,
                'y': len(hosts)
            })
    else:
        result = {
            'example': '_stat?res=hosts'
        }
    logger.debug(result)

    return jsonify(result), CODE_OK
