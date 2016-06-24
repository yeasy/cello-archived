import os
from flask import Flask

from common import log_handler, LOG_LEVEL
#from resources import action_v1
from resources import action_v1, action_v2

app = Flask(__name__, static_folder='static', template_folder='templates')

app.config.from_object('config.DevelopmentConfig')
app.config.from_envvar('POOLMANAGER_CONFIG_FILE', silent=True)

app.logger.addHandler(log_handler)
app.logger.setLevel(LOG_LEVEL)

app.register_blueprint(action_v1)
app.register_blueprint(action_v2)

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=80,
        debug=os.environ.get('DEBUG', app.config.get("DEBUG", True)),
        threaded=True
    )
