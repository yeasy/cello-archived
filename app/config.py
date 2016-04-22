import logging

class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE_URI = 'sqlite://:memory:'
    MONGO_URI = 'mongo:27017/test'
    SECRET_KEY = '?\xbf,\xb4\x8d\xa3"<\x9c\xb0@\x0f5\xab,w\xee\x8d$0\x13\x8b83'
    LOG_LEVEL = logging.DEBUG


class ProductionConfig(Config):
    DATABASE_URI = 'mysql://user@localhost/foo'
    MONGO_URI = 'mongo:27017/product'
    LOG_LEVEL = logging.INFO


class DevelopmentConfig(Config):
    DEBUG = True
    MONGO_URI = 'mongo:27017/dev'
    LOG_LEVEL = logging.DEBUG


class TestingConfig(Config):
    TESTING = True
    LOG_LEVEL = logging.DEBUG
