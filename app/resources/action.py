import __future__
from flask_restful import reqparse, Resource

from logging import getLogger

logger = getLogger(__name__)


parser = reqparse.RequestParser()
parser.add_argument('user_id', required=True, type=str, help='user id should be str')


class ApplyRoute(Resource):
    def get(self):
        args = parser.parse_args(strict=True)
        logger.warn("userid="+args["user_id"])
        return {"user_id": args["user_id"]}


class DropRoute(Resource):
    def get(self, user_id):
        args = parser.parse_args(strict=True)
        return {"user_id": args["user_id"]}
