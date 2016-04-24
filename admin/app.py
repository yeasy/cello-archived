import logging
from flask import Flask
from flask_restful import Api


app = Flask(__name__)
api = Api(app, prefix='/admin')

# app.config.from_envvar('POOLMANAGER_CONFIG')
app.config.from_object('config.DevelopmentConfig')

app.logger.setLevel(app.config.get("LOG_LEVEL", logging.INFO))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=app.config.get("DEBUG", True))
