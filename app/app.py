from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

from resources import ClusterRoute, ClustersRoute


app = Flask(__name__)
api = Api(app)
api.add_resource(ClustersRoute, '/clusters')

api.add_resource(ClusterRoute, '/cluster/<cluster_id>')

# app.config.from_envvar('POOLMANAGER_CONFIG')
app.config.from_object('config.DevelopmentConfig')


@app.route('/', methods=['GET'])
def index():
    return {}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)