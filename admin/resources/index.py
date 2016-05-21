import logging
import os
import sys

from flask import Blueprint, render_template
from flask import request as r

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from common import log_handler, LOG_LEVEL, CONSENSUS_TYPES

logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
logger.addHandler(log_handler)

from modules import cluster_handler, host_handler

index = Blueprint('index', __name__)


@index.route('/', methods=['GET'])
@index.route('/admin', methods=['GET'])
@index.route('/index', methods=['GET'])
def show():
    logger.info("/clusters action=" + r.method)
    hosts = list(host_handler.list())
    available_hosts = list(filter(
        lambda e: e["status"] == "active"
                  and len(e["clusters"]) < e["capacity"], hosts))
    clusters_active = len(list(cluster_handler.list(collection="active")))
    clusters_released = len(list(cluster_handler.list(collection="released")))

    #return render_template("test.html")
    return render_template("index.html", hosts=hosts,
                           available_hosts=available_hosts,
                           clusters_active=clusters_active,
                           clusters_released=clusters_released,
                           consensus_types=CONSENSUS_TYPES)