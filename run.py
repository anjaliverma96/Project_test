

"""Enables the command line execution of multiple modules within src/
This module combines the argparsing of each module within src/ and enables the execution of the corresponding scripts
so that all module imports can be absolute with respect to the main project directory.

Command to add databse schema in data folder in the project repository 
python run.py create_db
Command to add database schema in RDS
python run.py create_db --where AWS

Command to run app
python run.py run_app
"""

import os
import argparse
import logging
import logging.config
import yaml

with open(os.path.join("config","config.yml"), "r") as f:
    config = yaml.safe_load(f)

# The logging configurations are called from local.conf
# logging.config.fileConfig(os.path.join("config","logging_local.conf"))
# logger = logging.getLogger(config['logging']['LOGGER_NAME'])


#import necessary functions from src modules
from src.data_model import create_db

from app.views import run_app



if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Data processes")
    subparsers = parser.add_subparsers()

    # Sub-parser for creating a database
    sb_create = subparsers.add_parser("create_db", description="Create database to track usage logs")
    sb_create.add_argument("--where", default="Local", help="'Local' or 'AWS'. Seeks variables from environment for AWS by default")
    sb_create.set_defaults(func=create_db)

    # Sub-parser for starting the app
    sb_run_app = subparsers.add_parser("run_app", description="Starts the app")
    sb_run_app.set_defaults(func=run_app)

    args = parser.parse_args()
    args.func(args)






