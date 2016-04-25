from flask import Blueprint, request, jsonify, render_template

import os
import sys

import logging
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from common import log_handler
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(log_handler)

from modules import cluster_handler

index = Blueprint('index', __name__, url_prefix='/admin')


@index.route('/', methods=['GET'])
def show():
    return render_template("index.html", items=cluster_handler.list())


