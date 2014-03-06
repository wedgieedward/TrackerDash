"""
helper functions for basic database methods
"""
import logging
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure


def is_mongo_running():
    """
    tries to connect to a running mongo instance.
    if we can connect to one
    """
    logging.info("Trying to make a connection to a mongodb instance")
    try:
        MongoClient()
        logging.debug("Connection to running mongod instance established")
        return True
    except ConnectionFailure:
        logging.debug("Could not connect to a mongodb instance")
        return False


if __name__ == '__main__':
    print is_mongo_running()
