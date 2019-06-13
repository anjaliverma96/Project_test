

import os
MODE='AWS' #'local' or 'AWS' #change as necessary
#BUCKET_NAME='jokerecommender' #Necessary if MODE = 'AWS'

DEBUG = True
LOGGING_CONFIG = "config/logging_local.conf"

PORT = 3000
APP_NAME = "jokerecommender"
HOST = "127.0.0.1"


SECRET_KEY = 'reallyhardtoguesskey'
dbidentifier = 'anjalivermadb'
DATABASE_USERNAME = os.environ.get("MYSQL_USER")

DATABASE_PASSWORD = 'Positivesuccessful1!'
DATABASE_NAME = 'msia423'
DATABASE_ADDRESS = 'mysql-nw-anjaliverma.cyal1kueh9e9.us-east-2.rds.amazonaws.com'
DATABASE_URI = 'mysql+pymysql://%s:%s@%s/%s?use_unicode=1&charset=utf8' % (DATABASE_USERNAME,DATABASE_PASSWORD,DATABASE_ADDRESS,DATABASE_NAME)

if MODE == 'AWS':
    # SQLALCHEMY_DATABASE_URI = "{}://{}:{}@{}:{}/{}".\
    # format(conn_type, user, password, host, port, DATABASE_NAME)
    SQLALCHEMY_DATABASE_URI = DATABASE_URI
else:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../data/msia423.db'

SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_ECHO = False

