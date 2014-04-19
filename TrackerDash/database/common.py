"""
helper functions for basic database methods
"""
import logging

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from TrackerDash.constants import ESSENTIAL_COLLECTIONS
from TrackerDash.database.demo_data import DEMO_DATA
from TrackerDash.database.mongo_accessor import MongoAccessor


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


def is_mongo_configured(accessor):
    """
    works out if mongodb is configured to run with trackerdash
    i.e. first time running
    """
    return accessor.verify_essential_collections_present()


def add_demo_data(accessor):
    """
    should not be called by the app
    add demo dashboard data to the database
    """
    for collection, document in DEMO_DATA:
        accessor.add_document_to_collection(collection, document)


def remove_demo_data():
    """
    go through the configured demo data and remove it from the database:
    """
    accessor = MongoAccessor()
    for collection, document in DEMO_DATA:
        accessor.remove_documents_by_query(collection, document)


def get_dashboard_names(accessor):
    """
    given an instance of an accessor, get the configured dashboard names
    """
    dash_documents = accessor.get_all_documents_from_collection("dashboard")
    dash_names = [dash["name"] for dash in dash_documents]
    return dash_names


def get_configured_data_sources(accessor):
    """
    data sources are collections that are not explicitly created at startup
    we have to assume that any collection configured that is no a system or app collection
    is a data_source
    """
    collections = accessor.get_local_collections()
    data_sources = [
        collection for collection in collections if collection not in (
            ESSENTIAL_COLLECTIONS)]
    return data_sources
