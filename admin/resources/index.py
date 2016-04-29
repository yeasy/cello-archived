import logging
import os
import sys

from flask import Blueprint, render_template

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from common import log_handler, LOG_LEVEL

logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
logger.addHandler(log_handler)

from modules import cluster_handler

index = Blueprint('index', __name__)


@index.route('/', methods=['GET'])
@index.route('/admin', methods=['GET'])
@index.route('/index', methods=['GET'])
@index.route('/home', methods=['GET'])
def show():
    return render_template("index.html", items=cluster_handler.list())
