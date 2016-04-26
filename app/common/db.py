from pymongo import MongoClient

mongo_client = MongoClient('mongodb://mongo:27017/')

db = mongo_client['dev']
