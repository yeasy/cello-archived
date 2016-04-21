import __future__
from flask_restful import reqparse, abort, Api, Resource

parser = reqparse.RequestParser()
parser.add_argument('task')


# A single block chain, meaning a single hyperledger cluster
class Chain(Resource):
    def get(self, chain_id):
        print(chain_id)
        return {}

    def post(self):
        args = parser.parse_args()
        return {}, 201

    def delete(self, todo_id):
        return '', 204