import unittest

from TrackerDash.database.mongo_accessor import MongoAccessor

TEST_DATABASE = "TrackerDashTEST"


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
