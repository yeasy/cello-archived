import logging

from common import log_handler
from flask import Flask, render_template
from resources import index, cluster

app = Flask(__name__, static_folder='static', template_folder='templates')

app.config.from_object('config.DevelopmentConfig')
app.config.from_envvar('POOLMANAGER_CONFIG_FILE', silent=True)

app.logger.setLevel(app.config.get("LOG_LEVEL", logging.INFO))
app.logger.addHandler(log_handler)

app.register_blueprint(index)
app.register_blueprint(cluster)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=app.config.get("DEBUG", True))
