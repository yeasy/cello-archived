import os

from pymongo import MongoClient

MONGO_URL = os.environ.get('MONGO_URL', None) or 'mongodb://mongo:27017'
MONGO_COLLECTION = os.environ.get('MONGO_COLLECTION', None) or 'dev'

mongo_client = MongoClient(MONGO_URL)
db = mongo_client[MONGO_COLLECTION]
