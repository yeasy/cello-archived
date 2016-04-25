import logging
from flask import Flask

from resources import index, cluster

app = Flask(__name__)

app.config.from_object('config.DevelopmentConfig')
app.config.from_envvar('POOLMANAGER_CONFIG_FILE', silent=True)

app.logger.setLevel(app.config.get("LOG_LEVEL", logging.INFO))

app.register_blueprint(index)
app.register_blueprint(cluster)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=app.config.get("DEBUG", True))
