import os
import logging
import logging.config

from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

import yaml
import argparse

import getpass
import pymysql

logger = logging.getLogger()

Base = declarative_base()

class Ratings_Log(Base):

    """Create a data model for the database to be set up for capturing user input

    """

    __tablename__ = 'ratings_log'

    id = Column(Integer, primary_key=True)
    joke = Column(String(1000), unique=False, nullable=False)
    rating = Column(Integer, unique=False, nullable=True)


    def __repr__(self):
        ratings_log_repr = "<Ratings_Log(id='%i', joke ='%i', rating = '%i')>"
        return ratings_log_repr % (self.id, self.joke, self.rating)


def create_db(args):
    """Creates a database with the data models inherited from `Base` (Ratings_Log).

    Args:
        args: Argparse args - include args.

    Returns:
        None
    """
    with open(os.path.join("config","config.yml"), "r") as f:
        config = yaml.safe_load(f)

    logger.debug('Running the create_db function')
    
    if args.where == "Local":
        try:
            logger.info('Creating a local database at {}'.format(config['db_config']['SQLALCHEMY_DATABASE_URI']))
            engine = create_engine(config['db_config']['SQLALCHEMY_DATABASE_URI'])
            logger.debug('Database engine successfully created.')            
        except Exception as e:
            logger.error(e)
            
    elif args.where == "AWS":
        try:
            
            logger.info('Creating an RDS database based on environment variables: MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT, MYSQL_DB.')
            SECRET_KEY = 'reallyhardtoguesskey'
            dbidentifier = 'anjalivermadb'
            DATABASE_USERNAME = 'root'
            DATABASE_PASSWORD = 'Positivesuccessful1!'
            DATABASE_NAME = 'msia423'
            DATABASE_ADDRESS = 'mysql-nw-anjaliverma.cyal1kueh9e9.us-east-2.rds.amazonaws.com'
            DATABASE_URI = 'mysql+pymysql://%s:%s@%s/%s?use_unicode=1&charset=utf8' % (DATABASE_USERNAME,DATABASE_PASSWORD,DATABASE_ADDRESS,DATABASE_NAME)
            engine_string = DATABASE_URI
            # conn_type = "mysql+pymysql"
            # user = os.environ.get("MYSQL_USER")
            # password = os.environ.get("MYSQL_PASSWORD")
            # host = os.environ.get("MYSQL_HOST")
            # port = os.environ.get("MYSQL_PORT")
            # db_name = os.environ.get("MYSQL_DB")
            # engine_string = "{}://{}:{}@{}:{}/{}".format(conn_type, user, password, host, port, db_name)

        
            logger.debug('Creating database now.')    
            engine = create_engine(engine_string)            
            logger.debug('Database engine successfully created.')
        
        except Exception as e:
            logger.error("Database engine cannot be created. Kindly check the configurations and try again.")
            logger.error(e)
    
    else:
        raise ValueError('Kindly check the arguments and rerun. To understand different arguments, run `python run.py --help`')
    
    if args.where in ["AWS", "Local"]:    
        try:
            Base.metadata.drop_all(engine)
            Base.metadata.create_all(engine)
            logger.info('Database successfully created.')            
    
        except Exception as e:
            logger.error("Database could not be created. Kindly check the configurations and try again.")
            logger.error(e)