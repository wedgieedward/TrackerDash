"""
Client for accessing the mongodatabase
"""
import logging
import unittest

import pymongo

from TrackerDash.database.demo_data import DEMO_DATA

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

    def reset_all(self):
        """
        warning: deletes all collections and re-adds the vital ones
        """
        for collection in self.get_local_collections():
            self.delete_collection(collection)
        self.add_essential_collections()

    def add_essential_collections(self):
        """
        these are the essential collections needed for trackerdash to operate
        """
        for collection in ESSENTIAL_COLLECTIONS:
            self.create_collection(collection)

    def verify_essential_collections_present(self):
        """
        """
        present = True
        all_collections = self.get_local_collections()
        for collection in ESSENTIAL_COLLECTIONS:
            if collection not in all_collections:
                present = False

        return present

    def get_raw_database(self):
        """
        returns the pymongo database instance this class wraps
        """
        return self.database

    def get_all_collections(self):
        """
        return a list of all the collections in the database
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
        return self.database[collection_name]

    def add_document_to_collection(self, collection_name, document):
        """
        add a json document to a specified collection
        """
        logging.debug("Inseting %r into collection %s" % (document, collection_name))
        collection = self.get_collection(collection_name)
        collection.insert(document)

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

    def add_demo_data(self):
        """
        should not be called by the app
        add demo dashboard data to the database
        """
        for collection, document in DEMO_DATA:
            self.add_document_to_collection(collection, document)


class TestAccessor(MongoAccessor):
    database_name = TEST_DATABASE

    def __init__(self):
        super(TestAccessor, self).__init__()


class AccessorSanity(unittest.TestCase):
    """
    """
    def setUp(self):
        test_accessor = TestAccessor()
        for collection in test_accessor.get_local_collections():
            test_accessor.delete_collection(collection)

    def test_inheritance(self):
        """
        tests that the object inheretance works as expected
        """
        live_accessor = MongoAccessor()
        test_accessor = TestAccessor()

        # Count how many collections there are of each instance
        before_live = len(live_accessor.get_local_collections())
        before_test = len(test_accessor.get_local_collections())

        # add some collections to the test_accessor and
        # ensure they do not appear on the live_accessor
        test_accessor.create_collection("test_inheritance1")
        test_accessor.create_collection("test_inheritance2")
        test_accessor.create_collection("test_inheritance3")

        # get latest numbers
        after_live = len(live_accessor.get_local_collections())
        after_test = len(test_accessor.get_local_collections())

        self.assertEquals(before_live, after_live)
        self.assertNotEquals(before_test, after_test)

        for collection in test_accessor.get_local_collections():
            test_accessor.delete_collection(collection)

    def test_post_to_unknown_collection(self):
        """
        The api will have the ability to post to any named graph,
        even if it doesn't exist.
        """
        accessor = TestAccessor()
        collection = "unknown"
        collections = accessor.get_local_collections()
        self.assertNotIn(collection, collections)
        num_collections = len(collections)
        accessor.add_document_to_collection(collection, {"key": "value"})
        collections = accessor.get_local_collections()
        self.assertNotEquals(len(collections), num_collections)
        num_docs = accessor.get_number_of_documents_in_collection("unknown")
        self.assertEquals(num_docs, 1)


if __name__ == '__main__':
    unittest.main()
