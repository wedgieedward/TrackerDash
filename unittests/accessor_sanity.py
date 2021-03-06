from copy import deepcopy
from datetime import datetime
from datetime import timedelta
import unittest

from TrackerDash.database.mongo_accessor import MongoAccessor
from TrackerDash.database.mongo_accessor import TestAccessor


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

    def test_get_unknown_collection(self):
        """
        tests the behaviour of trying to get a collection that does not exist
        """
        accessor = TestAccessor()
        collection = "unknown"
        collections = accessor.get_local_collections()
        self.assertNotIn(collection, collections)
        self.assertRaises(LookupError, accessor.get_collection, collection)

    def test_get_documents_by_time(self):
        """
        tests that we can query data within the last x amount of days
        """
        accessor = TestAccessor()
        collection = "timequerycollection"
        days = 30
        self.add_data_over_x_days(collection, days)
        docs_in_collection = accessor.get_number_of_documents_in_collection(
            collection)
        self.assertEquals(docs_in_collection, days)
        docs_in_last_seven_days = accessor.get_all_documents_created_in_last(
            collection, weeks=1)
        self.assertEquals(len(docs_in_last_seven_days), 7)
        docs_in_last_seven_days = accessor.get_all_documents_created_in_last(
            collection, days=7)
        self.assertEquals(len(docs_in_last_seven_days), 7)
        docs_in_the_last_eight_days = (
            accessor.get_all_documents_created_in_last(
                collection, weeks=1, days=1))
        self.assertEquals(len(docs_in_the_last_eight_days), 8)
        docs_in_the_last_eight_days = (
            accessor.get_all_documents_created_in_last(
                collection, days=8))
        self.assertEquals(len(docs_in_the_last_eight_days), 8)

    def test_create_duplicate_collection(self):
        """
        tests the behaviour of trying to create the same collection twice
        """
        accessor = TestAccessor()
        collection = "unknown"
        collections = accessor.get_local_collections()
        self.assertNotIn(collection, collections)
        accessor.create_collection(collection)
        collections = accessor.get_local_collections()
        self.assertIn(collection, collections)
        self.assertRaises(NameError, accessor.create_collection, collection)

    def test_get_document_that_doesnt_exist(self):
        """
        """
        accessor = TestAccessor()
        collection = "testcollection"
        accessor.create_collection(collection)
        result = accessor.get_documents_by_query(collection, {"foo": "bar"})
        self.assertEquals(result, [])

    def test_get_last_document_inserted(self):
        accessor = TestAccessor()
        collection = "testcollection"
        number_of_docs_to_add = 5
        for x in range(number_of_docs_to_add):
            document = {"value": x}
            accessor.add_document_to_collection(collection, document)
        number_of_docs_in_collection = (
            accessor.get_number_of_documents_in_collection(collection))
        self.assertEquals(number_of_docs_in_collection, number_of_docs_to_add)
        last_doc = accessor.get_last_document_inserted(collection)
        self.assertIsNotNone(last_doc)
        self.assertEquals(last_doc["value"], number_of_docs_to_add - 1)

    def test_redundant_post(self):
        accessor = TestAccessor()
        collection = "redundencytest"
        accessor.add_document_to_collection_redundant(
            collection, {"test": 1, "foo": "bar"}, 60)
        accessor.add_document_to_collection_redundant(
            collection, {"test": 1, "foo": "bar"}, 60)
        accessor.add_document_to_collection_redundant(
            collection, {"test": 1, "foo": "bar"}, 60)
        accessor.add_document_to_collection_redundant(
            collection, {"test": 1, "foo": "bar"}, 60)
        accessor.add_document_to_collection_redundant(
            collection, {"test": 1, "foo": "bar"}, 60)
        accessor.add_document_to_collection_redundant(
            collection, {"test": 1, "foo": "bar"}, 60)
        accessor.add_document_to_collection_redundant(
            collection, {"test": 1, "foo": "bar"}, 60)
        self.assertEquals(
            accessor.get_number_of_documents_in_collection(collection), 1)
        accessor.add_document_to_collection_redundant(
            collection, {"test": 2, "foo": "bar"}, 60)
        accessor.add_document_to_collection_redundant(
            collection, {"test": 2, "foo": "bar"}, 60)
        accessor.add_document_to_collection_redundant(
            collection, {"test": 2, "foo": "bar"}, 60)
        accessor.add_document_to_collection_redundant(
            collection, {"test": 2, "foo": "bar"}, 60)
        accessor.add_document_to_collection_redundant(
            collection, {"test": 2, "foo": "bar"}, 60)
        accessor.add_document_to_collection_redundant(
            collection, {"test": 2, "foo": "bar"}, 60)
        accessor.add_document_to_collection_redundant(
            collection, {"test": 2, "foo": "bar"}, 60)
        accessor.add_document_to_collection_redundant(
            collection, {"test": 2, "foo": "bar"}, 60)
        self.assertEquals(
            accessor.get_number_of_documents_in_collection(collection), 2)
        accessor.add_document_to_collection_redundant(
            collection, {"test": 1, "foo": "bar"}, 60)
        accessor.add_document_to_collection_redundant(
            collection, {"test": 2, "foo": "bar"}, 60)
        self.assertEquals(
            accessor.get_number_of_documents_in_collection(collection), 4)

    def add_data_over_x_days(self, collection_name, days):
        """
        creates mock data
        """
        accessor = TestAccessor()
        for x in range(days):
            timestamp = (datetime.utcnow() - timedelta(days=x))
            document = {
                "days": x,
                "__date": timestamp
            }
            accessor.add_document_to_collection(collection_name, document)

    def test_date_gets_added_to_record(self):
        """
        modify_document_for_database is meant to add a utc date to each
        inserted record
        """
        accessor = TestAccessor()
        document = {u"test": u"document"}
        accessor.add_document_to_collection(
            "test_collection", deepcopy(document))

        saved_document = accessor.get_one_document_by_query(
            'test_collection', document)
        self.assertIsNotNone(saved_document)
        self.assertNotEquals(saved_document, document)
        self.assertIn("__date", saved_document)
        del saved_document["__date"]
        del saved_document["_id"]
        self.assertEquals(saved_document, document)

    def test_get_all_documents_from_collection(self):
        """
        tests that we can save and get all the documents in a collection
        """
        accessor = TestAccessor()
        document = {"test": "document"}
        collection = "test_collection"
        for x in range(1, 20):
            accessor.add_document_to_collection(collection, deepcopy(document))
            recs = accessor.get_all_documents_from_collection(collection)
            self.assertEquals(len(recs), x)
            recs = accessor.get_documents_by_query(
                collection, deepcopy(document))
            self.assertEquals(len(recs), x)

    def test_remove_documents_by_query(self):
        """
        tests that we delete by query correctly
        """
        accessor = TestAccessor()
        collection = "test_collection"
        max_val = 20
        for x in range(1, max_val):
            document = {"key": x}
            accessor.add_document_to_collection(collection, document)
            self.assertEquals(
                accessor.get_number_of_documents_in_collection(collection), x)

        for x in range(1, max_val)[::-1]:  # reverse list
            document = {"key": x}
            self.assertEquals(
                accessor.get_number_of_documents_in_collection(collection), x)
            accessor.remove_documents_by_query(collection, document)
            self.assertEquals(
                accessor.get_number_of_documents_in_collection(collection),
                x - 1)


if __name__ == '__main__':
    unittest.main()
