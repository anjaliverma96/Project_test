

"""Enables the command line execution of multiple modules within src/
This module combines the argparsing of each module within src/ and enables the execution of the corresponding scripts
so that all module imports can be absolute with respect to the main project directory.

Command to load data into S3 bucket 
python run.py loadS3
Command to add databse schema data folder in the project repository 
python run.py createSqlite
Command to add database schema in RDS
python run.py createRDS
"""

import os
import argparse
import logging.config
logging.config.fileConfig("config/logging/local.conf")
logger = logging.getLogger("jokerecommender")

# #import necessary functions from src modules

# from src.downloadData import load_data
# from src.add_schema import create_sqlite_db, create_rds_db

# #import necessary variables from config file

# from config import BUCKET_NAME, SQLALCHEMY_DATABASE_URI, DATABASE_NAME

from app.views import run_app


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Data processes")
    subparsers = parser.add_subparsers()


    # Sub-parser for starting the app
    sb_run_app = subparsers.add_parser("run_app", description="Starts the app")
    sb_run_app.set_defaults(func=run_app)

    args = parser.parse_args()
    args.func(args)






