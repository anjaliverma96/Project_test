import os
SECRET_KEY = 'reallyhardtoguesskey'
dbidentifier = 'anjalivermadb'
DATABASE_USERNAME = 'root'
DATABASE_PASSWORD = 'Positivesuccessful1!'
DATABASE_NAME = 'msia423'
DATABASE_ADDRESS = 'mysql-nw-anjaliverma.cyal1kueh9e9.us-east-2.rds.amazonaws.com'
DATABASE_URI = 'mysql+pymysql://%s:%s@%s/%s?use_unicode=1&charset=utf8' % (DATABASE_USERNAME,DATABASE_PASSWORD,DATABASE_ADDRESS,DATABASE_NAME)
SQLALCHEMY_DATABASE_URI = DATABASE_URI