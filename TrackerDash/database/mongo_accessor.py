"""
Client for accessing the mongodatabase
"""
from datetime import datetime
from datetime import timedelta
import logging
from bson import objectid
import pymongo

LIVE_DATABASE = "TrackerDashApp"
TEST_DATABASE = "TrackerDashTEST"

ESSENTIAL_COLLECTIONS = (
    "showreel",
    "dashboard",
    "graph",
    "config")


class MongoAccessor(object):
    """
    class operations for interacting with mongodb
    """
    database_name = LIVE_DATABASE

    def __init__(self):
        self.client = pymongo.MongoClient()
        self.database = self.client[self.database_name]

    # Database Methods
    def get_raw_database(self):
        """
        returns the pymongo database instance this class wraps
        """
        return self.database

    def reset_all(self):
        """
        warning: deletes all collections and re-adds the vital ones
        """
        for collection in self.get_local_collections():
            self.delete_collection(collection)
        self.add_essential_collections()

    def add_essential_collections(self):
        """
        add the minimum collections required for TrackerDash to operate
        """
        for collection in ESSENTIAL_COLLECTIONS:
            self.create_collection(collection)

    def verify_essential_collections_present(self):
        """
        returns true if all the collections required to operate are present in the database
        """
        present = True
        all_collections = self.get_local_collections()
        for collection in ESSENTIAL_COLLECTIONS:
            if collection not in all_collections:
                present = False

        return present

    # Collection Operations
    def get_all_collections(self):
        """
        return a list of all the collections in the database including system collections
        """
        return self.database.collection_names(include_system_collections=True)

    def get_local_collections(self):
        """
        return a list of all the non system collections in the database
        """
        return self.database.collection_names(include_system_collections=False)

    def create_collection(self, collection_name):
        """
        given a collection name, add the collection to the database
        """
        logging.debug("creating collection %s" % collection_name)
        try:
            self.database.create_collection(collection_name)
        except pymongo.errors.CollectionInvalid:
            logging.error("collection %s already exists" % collection_name)

    def delete_collection(self, collection_name):
        """
        given a collection name or collection object,
        drop the collection from the database
        """
        logging.debug("deleting collection %s" % collection_name)
        return self.database.drop_collection(collection_name)

    def get_collection(self, collection_name):
        """
        returns a collection object
        """
        if collection_name in self.get_all_collections():
            return self.database[collection_name]
        else:
            raise LookupError("%s not found in database" % collection_name)

    def get_number_of_documents_in_collection(self, collection_name):
        """
        given a collection_name, get the number of documents in collection
        """
        collection = self.get_collection(collection_name)
        return collection.count()

    def get_all_documents_from_collection(self, collection_name):
        """
        get all the documents in this collection
        """
        collection = self.get_collection(collection_name)
        documents = [doc for doc in collection.find()]
        return documents

    # Document Methods
    def add_document_to_collection(self, collection_name, document):
        """
        add a json document to a specified collection
        """
        logging.debug("Inseting %r into collection %s" % (document, collection_name))
        try:
            collection = self.get_collection(collection_name)
            collection.insert(document)
        except LookupError:
            self.create_collection(collection_name)
            self.add_document_to_collection(collection_name, document)

    def get_documents_by_query(self, collection_name, query):
        """
        queries a collection
        """
        collection = self.get_collection(collection_name)
        documents = [doc for doc in collection.find(query)]
        return documents

    def get_one_document_by_query(self, collection_name, query):
        """
        does a find_one on a collection based on query
        """
        collection = self.get_collection(collection_name)
        document = collection.find_one(query)
        return document

    def get_all_documents_created_in_last(self,
                                          collection_name,
                                          weeks=0,
                                          days=0,
                                          hours=0,
                                          minutes=0):
        """
        Given a collection and a time interval, get all the documents in that collection
        created after that defined time interval
        """
        timestamp_query = datetime.now() - timedelta(weeks=weeks,
                                                     days=days,
                                                     hours=hours,
                                                     minutes=minutes)
        query = {"_id": {"$gt": objectid.ObjectId.from_datetime(timestamp_query)}}
        return self.get_documents_by_query(collection_name, query)


class TestAccessor(MongoAccessor):
    database_name = TEST_DATABASE

    def __init__(self):
        super(TestAccessor, self).__init__()
