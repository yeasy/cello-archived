import __future__
from flask_restful import reqparse, Resource

parser = reqparse.RequestParser()
parser.add_argument('task')


# clusters list
class ClustersRoute(Resource):
    def get(self, chain_id):
        return {}


# A single hyperledger cluster
class ClusterRoute(Resource):
    def get(self, chain_id):
        print(chain_id)
        return {}

    def post(self):
        args = parser.parse_args()
        return {}, 201

    def delete(self, todo_id):
        return '', 204