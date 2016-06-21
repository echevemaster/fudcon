# -*- coding: utf-8 -*-
import os
import datetime
# Belonging to the path of  sqlite development database.
basedir = os.path.abspath(os.path.dirname(__file__))
engine = 'sqlite'  # sqlite, Mysql, postgres and so on.
db_name = 'fudcon.db'
db_user = ''
db_password = ''
db_server = 'localhost'  # Usually, localhost


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SQLALCHEMY_ECHO = True
    FAS_OPENID_ENDPOINT = 'http://id.fedoraproject.org/'
    FAS_CHECK_CERT = True
    FUDCON_NAME = 'FUDCon Puno'
    ADMIN_GROUP = ['fudcon']
    ITEMS_PER_PAGE = 10
    UPLOADS_FOLDER = os.path.realpath('.') + '/fudcon/static/uploads'
    TALKS_FOLDER = os.path.realpath('.') + '/fudcon/static/slides'
    OPEN_WORKSHOP_AND_BARCAMPS = datetime.datetime(2016, 10, 13)
    ALLOWED_EXTENSIONS = set(['jpeg', 'jpg', 'gif', 'png',
                             'txt', 'pdf'])
    SOCIAL_AUTH_LOGIN_URL = '/login'
    SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/done'
    SOCIAL_AUTH_USER_MODEL = 'fudcon.modules.users.models.User'
    SOCIAL_AUTH_AUTHENTICATION_BACKENDS = (
        'social.backends.google.GoogleOpenId',
        'social.backends.twitter.TwitterOAuth',
        'social.backends.fedora.FedoraOpenId',
        'social.backends.facebook.FacebookOAuth2',
        )
    SOCIAL_AUTH_TWITTER_KEY = 'Kd9WxF07GKqjKZm9Rcjdj8MHx'
    SOCIAL_AUTH_TWITTER_SECRET = '8NDXh4rsPe5uSUfavfnbrwJp837GZKxpfBX4CAVyRbP35Xhs2c'
    SOCIAL_AUTH_FACEBOOK_KEY = '647259998720994'
    SOCIAL_AUTH_FACEBOOK_SECRET = '4ff1d136e25c8242908c37ea5c10d338'
    SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
    SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {'locale': 'es_ES'}
    


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = '{0}://{1}:{2}@{3}/{4}'.format(engine,
                                                             db_user,
                                                             db_password,
                                                             db_server,
                                                             db_name)
    DATABASE_CONNECT_OPTIONS = {}
    SECRET_KEY = 'key'
    CSRF_SESSION_KEY = "somethingimpossibletoguess"


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = engine + ':///' + os.path.join(basedir,
                                                             db_name)
    DATABASE_CONNECT_OPTIONS = {}
    SQLALCHEMY_ECHO = True
    SECRET_KEY = 'This string will be replaced with a proper key in production'
    CSRF_SESSION_KEY = "somethingimpossibletoguess"


class TestingConfig(Config):
    TESTING = True
