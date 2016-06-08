from flask import Flask

from common import log_handler, LOG_LEVEL
from resources import action

app = Flask(__name__, static_folder='static', template_folder='templates')

app.config.from_object('config.DevelopmentConfig')
app.config.from_envvar('POOLMANAGER_CONFIG_FILE', silent=True)

app.logger.addHandler(log_handler)
app.logger.setLevel(LOG_LEVEL)

app.register_blueprint(action)

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=80,
        debug=app.config.get("DEBUG", True),
        threaded=True
    )
