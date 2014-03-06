"""
helper functions for basic database methods
"""
import logging

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from mongo_accessor import MongoAccessor


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


def is_mongo_configured():
    """
    works out if mongodb is configured to run with trackerdash
    i.e. first time running
    """
    accessor = MongoAccessor()
    return accessor.verify_essential_collections_present()


if __name__ == '__main__':
    print "Mongo Running: %s" % is_mongo_running()
    print "Mongo Configured For TrackerDash: %s" % is_mongo_configured()
