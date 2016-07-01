import logging
import os
import sys

from flask import Blueprint, render_template
from flask import request as r

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from common import log_handler, LOG_LEVEL, CONSENSUS_PLUGINS, \
    CONSENSUS_MODES, HOST_TYPES, LOG_TYPES, CLUSTER_SIZES, request_debug
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
    request_debug(r, logger)
    hosts = list(host_handler.list(filter_data={}, validate=True))
    hosts.sort(key=lambda x: x["name"], reverse=False)
    hosts_active = list(filter(lambda e: e["status"] == "active", hosts))
    hosts_free = list(filter(
        lambda e: len(e["clusters"]) < e["capacity"], hosts_active))
    #hosts_available = list(filter(
    #    lambda e:  e["schedulable"] == "true", hosts_free))
    hosts_available = hosts_free
    clusters_active = len(list(cluster_handler.list(col_name="active")))
    clusters_released = len(list(cluster_handler.list(col_name="released")))
    clusters_free = len(list(cluster_handler.list(col_name="active",
                                                  filter_data={"user_id": ""})))

    clusters_temp = len(list(cluster_handler.list(col_name="active",
                                                  filter_data={"user_id":
                                                                   "/^__/"})))

    return render_template("index.html", hosts=hosts,
                           hosts_free=hosts_free, hosts_active=hosts_active,
                           hosts_available=hosts_available,
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
    logger.info("path={}, method={}".format(r.path, r.method))
    return render_template("about.html", author=author, version=version,
                           homepage=homepage)