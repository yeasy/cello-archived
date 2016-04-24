import logging
from flask import Flask

from common import log_handler
from resources import action

app = Flask(__name__)

app.config.from_object('config.DevelopmentConfig')
app.config.from_envvar('POOLMANAGER_CONFIG_FILE', silent=True)

app.logger.setLevel(app.config.get("LOG_LEVEL", logging.INFO))
app.logger.addHandler(log_handler)

app.register_blueprint(action)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=app.config.get("DEBUG", True))
