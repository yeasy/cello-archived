import __future__
from flask_restful import reqparse, Resource

parser = reqparse.RequestParser()


class AdminRoute(Resource):
    def get(self):
        return {}

