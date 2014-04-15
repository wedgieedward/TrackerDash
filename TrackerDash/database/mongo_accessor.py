"""
Client for accessing the mongodatabase
"""
from datetime import datetime
from datetime import timedelta
import logging

import pymongo

from TrackerDash.constants import ESSENTIAL_COLLECTIONS


LIVE_DATABASE = "TrackerDashApp"
TEST_DATABASE = "TrackerDashTEST"


class MongoAccessor(object):
    """
    class operations for interacting with mongodb
    """
    database_name = LIVE_DATABASE

    def __init__(self):
        self.client = pymongo.MongoClient()
        self.database = self.client[self.database_name]

    def get_date(self):
        """
        get an appropriate value to insert into mongodb to represent date
        """
        return datetime.utcnow()

    def get_date_x_ago(self, **date_info):
        """
        get a date **date_info time ago
        date_info is a dictionary of key values to represent the input to
        a time delta function
        """
        return (self.get_date() - timedelta(**date_info))

    def modify_document_for_database(self, document):
        """
        alter the document before inserting it into the database
        """
        # Add a __date field to the record (if it doesn't already exist)
        document["__date"] = document.get("__date", self.get_date())

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
        logging.info("creating collection %s" % collection_name)
        try:
            self.database.create_collection(collection_name)
        except pymongo.errors.CollectionInvalid:
            # logging.debug("collection %s already exists" % collection_name)
            raise NameError("name already exists")

    def delete_collection(self, collection_name):
        """
        given a collection name or collection object,
        drop the collection from the database
        """
        logging.info("deleting collection %s" % collection_name)
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
        This should be the only way a document is added to the collection.
        """
        logging.info("Inserting %r into collection %s" % (
            document, collection_name))
        try:
            collection = self.get_collection(collection_name)
            self.modify_document_for_database(document)
            collection.insert(document)
        except LookupError:
            logging.info(
                "Collection %s not found, creating now and trying again" % (
                    collection_name, ))
            self.create_collection(collection_name)
            self.add_document_to_collection(collection_name, document)

    def add_document_to_collection_redundant(self,
                                             collection_name,
                                             document,
                                             redundency_seconds):
        """
        will only add a new document if needed
        """
        try:
            documents_in_period = self.get_all_documents_created_in_last(
                collection_name, seconds=redundency_seconds)
            if len(documents_in_period) == 0:
                # no documents added in
                self.add_document_to_collection(collection_name, document)
            elif len(documents_in_period) >= 1:
                last_document_inserted = documents_in_period[-1]
                del last_document_inserted["_id"]
                del last_document_inserted["__date"]
                if last_document_inserted != document:
                    self.add_document_to_collection(collection_name, document)
            else:
                logging.info(
                    "Ignoring %r because an identical document "
                    "has been inserted into %r within the last %s seconds" % (
                        document, collection_name, redundency_seconds))
        except LookupError:
            # the collection hasn't even been created yet,
            # just add the document to it
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

    def get_last_document_inserted(self, collection_name):
        collection = self.get_collection(collection_name)
        document = collection.find().sort("_id", -1).limit(1)
        return document[0]

    def get_all_documents_created_in_last(self,
                                          collection_name,
                                          **kwargs):
        """
        Given a collection and a time interval, get all the documents in that collection
        created after that defined time interval
        """
        # months gets ignored intentionally
        timestamp = self.get_date_x_ago(**kwargs)
        query = {"__date": {"$gte": timestamp}}
        return self.get_documents_by_query(collection_name, query)

    def remove_documents_by_query(self, collection_name, query):
        """
        given a query, delete all documents that match it
        """
        collection = self.get_collection(collection_name)
        collection.remove(query)


class TestAccessor(MongoAccessor):
    database_name = TEST_DATABASE

    def __init__(self):
        super(TestAccessor, self).__init__()
