import logging
from flask import Flask
from flask_restful import Api

from common import log_handler
from resources import ClusterRoute, ClustersRoute, ApplyRoute, DropRoute


app = Flask(__name__)
api = Api(app, prefix='/v1')

api.add_resource(ClustersRoute, '/clusters')
api.add_resource(ClusterRoute, '/cluster/<cluster_id>')

api.add_resource(ApplyRoute, '/cluster_apply')
api.add_resource(DropRoute, '/cluster_drop')

# app.config.from_envvar('POOLMANAGER_CONFIG')
app.config.from_object('config.DevelopmentConfig')

app.logger.setLevel(app.config.get("LOG_LEVEL", logging.INFO))
app.logger.addHandler(log_handler)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=app.config.get("DEBUG", True))
