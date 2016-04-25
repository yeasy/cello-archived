import __future__

from flask import Blueprint, request, jsonify

from logging import getLogger

logger = getLogger(__name__)

action = Blueprint('action', __name__, url_prefix='/admin')


@action.route('/cluster_apply', methods=['GET'])
def cluster_apply():
    user_id = request.args.get("user_id", "")
    logger.warn("userid="+user_id)
    if not user_id:
        return jsonify({"user_id": "not provided"})
    else:
        return jsonify({"user_id": user_id})


@action.route('/cluster_drop', methods=['GET'])
def cluster_drop():
    user_id = request.args.get("user_id", "")
    logger.warn("userid="+user_id)
    if not user_id:
        return jsonify({"user_id": "not provided"})
    else:
        return jsonify({"user_id": user_id})
