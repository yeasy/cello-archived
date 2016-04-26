import __future__

from flask import Blueprint, request, jsonify

import logging

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from common import log_handler
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(log_handler)

action = Blueprint('action', __name__, url_prefix='/v1')


@action.route('/cluster_apply', methods=['GET'])
def cluster_apply():
    """
    Return a Cluster json body.
    """
    user_id = request.args.get("user_id", "")
    logger.warn("userid="+user_id)
    if not user_id:
        return jsonify({"user_id": "not provided"})
    else:
        return jsonify({"user_id": user_id})


@action.route('/cluster_release', methods=['GET'])
def cluster_release():
    user_id = request.args.get("user_id", "")
    logger.warn("userid="+user_id)
    if not user_id:
        return jsonify({"user_id": "not provided"})
    else:
        return jsonify({"user_id": user_id})
