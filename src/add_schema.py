
import argparse
import logging.config
import os
import sys
import flask
import sqlalchemy

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, MetaData

#set path to be able to access config.py

sys.path.append(os.path.abspath(os.path.join('..')))

#import necessary variables from config.py

from config import SQLALCHEMY_DATABASE_URI, DATABASE_NAME


logger = logging.getLogger(__name__)
logger.setLevel("INFO")

Base = declarative_base()


class UserRating(Base):

    """Create a data model for the database to be set up for capturing user input

    """

    __tablename__ = 'userrating'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=False, nullable=False)
    joke_id = Column(Integer, unique=False, nullable=False)
    rating = Column(Integer, unique=False, nullable=True)

    def __repr__(self):
        userrating_repr = "<UserRating(id='%i', user_id='%i', joke_id='%i', rating = '%i')>"
        return userrating_repr % (self.id, self.user_id, self.joke_id, self.rating)


class JokeDesc(Base):

    """Create a data model for the table JokeDesc

    """

    __tablename__ = 'jokedesc'

    joke_id = Column(Integer, primary_key=True)
    joke = Column(String(1000), unique=False, nullable=False)


    def __repr__(self):
        jokedesc_repr = "<JokeDesc(joke_id='%i', joke='%s')>"
        return jokedesc_repr % (self.joke_id, self.joke)

# Create table in sqlite database

def create_sqlite_db(args):
    """Creates an sqlite database with the data models inherited from `Base` .
    Args:
        args (argument from user): String defining SQLAlchemy connection URI in the form of
    Returns:
        None
    """

    engine = sqlalchemy.create_engine(args.engine_string)

    logger.info('SQLite database created')

    Base.metadata.create_all(engine)

    logger.info('Table created in SQLite database')

# Create table in RDS database

def create_rds_db(args):
    """Creates an rds table with the data models inherited from `Base` (UserLines).
        Args:
            args (argument from user): String defining RDS in the desrired form
        Returns:
            None
    """

    conn_type = "mysql+pymysql"
    user = os.environ.get("MYSQL_USER")
    password = os.environ.get("MYSQL_PASSWORD")
    host = os.environ.get("MYSQL_HOST")
    port = os.environ.get("MYSQL_PORT")
    engine_string = "{}://{}:{}@{}:{}/{}". \
        format(conn_type, user, password, host, port, DATABASE_NAME)

    engine = sqlalchemy.create_engine(engine_string)
    Base.metadata.create_all(engine)

    logger.info('Table created in RDS database')


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Data processes")
    subparsers = parser.add_subparsers()

    sub_process = subparsers.add_parser('createSqlite')
    sub_process.add_argument("--database", type=str, default=SQLALCHEMY_DATABASE_URI,
                             help="Connection uri for SQLALCHEMY")
    sub_process.set_defaults(func=create_sqlite_db)

    sub_process = subparsers.add_parser('createRDS')
    sub_process.add_argument("--database", type=str, default=DATABASE_NAME,
                             help="Database in RDS")
    sub_process.set_defaults(func=create_rds_db)

    args = parser.parse_args()
    args.func(args)