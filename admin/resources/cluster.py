import __future__
import os
import sys

from flask import jsonify

import logging
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from common import log_handler
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(log_handler)

cluster = Blueprint('cluster', __name__, url_prefix='/cluster')


@cluster.route('/', methods=['GET'])
def get():
    return jsonify({"cluster":"get"})

