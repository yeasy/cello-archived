import logging
import os
import sys

from flask import Blueprint, render_template
from flask import request as r

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from common import log_handler, LOG_LEVEL, CONSENSUS_PLUGINS, \
    CONSENSUS_MODES, HOST_TYPES, LOG_TYPES, CLUSTER_SIZES
from version import version, homepage, author

logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
logger.addHandler(log_handler)

from modules import cluster_handler, host_handler

index = Blueprint('index', __name__)


@index.route('/', methods=['GET'])
@index.route('/admin', methods=['GET'])
@index.route('/index', methods=['GET'])
def show():
    logger.info("path={}, action={}".format(r.path, r.method))
    hosts = list(host_handler.list(filter_data={}, validate=False))
    hosts.sort(key=lambda x: str(x["name"]), reverse=False)
    available_hosts = list(filter(
        lambda e: e["status"] == "active"
                  and len(e["clusters"]) < e["capacity"], hosts))
    clusters_active = len(list(cluster_handler.list(col_name="active")))
    clusters_released = len(list(cluster_handler.list(col_name="released")))
    clusters_free = len(list(cluster_handler.list(col_name="active",
                                                  filter_data={"user_id": ""})))

    clusters_temp = len(list(cluster_handler.list(col_name="active",
                                                  filter_data={"user_id":
                                                                   "/^__/"})))

    #return render_template("test.html")
    return render_template("index.html", hosts=hosts,
                           available_hosts=available_hosts,
                           clusters_active=clusters_active,
                           clusters_released=clusters_released,
                           clusters_free=clusters_free,
                           clusters_temp=clusters_temp,
                           cluster_sizes=CLUSTER_SIZES,
                           consensus_plugins=CONSENSUS_PLUGINS,
                           consensus_modes=CONSENSUS_MODES,
                           host_types=HOST_TYPES, log_types=LOG_TYPES)


@index.route('/about', methods=['GET'])
def about():
    logger.info("path={}, action={}".format(r.path, r.method))
    return render_template("about.html", author=author, version=version,
                           homepage=homepage)
