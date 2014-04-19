import unittest

from TrackerDash.database import common
from TrackerDash.database import demo_data
from TrackerDash.database.mongo_accessor import TestAccessor


class TestDatabaseCommon(unittest.TestCase):
    """
    test functionality of datbase common
    """

    accessor = TestAccessor()

    def setUp(self):
        for collection in self.accessor.get_local_collections():
            self.accessor.delete_collection(collection)

    def test_is_mongo_configured(self):
        """
        test common.is_mongo_configured
        """
        num_collections = len(self.accessor.get_local_collections())
        self.assertEquals(num_collections, 0)

        self.assertFalse(common.is_mongo_configured(self.accessor))
        self.accessor.add_essential_collections()
        num_collections = len(self.accessor.get_local_collections())
        self.assertNotEquals(num_collections, 0)

        self.assertTrue(common.is_mongo_configured(self.accessor))

    def test_add_demo_data(self):
        """
        asserts all the correct demo data is inserted
        """
        common.add_demo_data(self.accessor)

        # verify all demo data is present
        for collection, document in demo_data.DEMO_DATA:
            document = self.accessor.get_one_document_by_query(
                collection, document)
            self.assertIsNotNone(document)

    def test_get_dashboard_names(self):
        """
        tests the behaviour of get_dashboard_names
        """
        self.accessor.add_essential_collections()
        self.assertEquals(common.get_dashboard_names(self.accessor), [])

        self.accessor.add_document_to_collection(
            "dashboard", {"name": "test", "row_data": [["something"]]})
        dashboards = common.get_dashboard_names(self.accessor)
        self.assertEquals(len(dashboards), 1)
        self.assertIn('test', dashboards)

    def test_get_configured_data_sources(self):
        """
        tests the behaviour of get_configured_data_sources
        """
        data_sources = common.get_configured_data_sources(self.accessor)
        self.assertEquals(len(data_sources), 0)
        self.assertEquals(data_sources, [])

        self.accessor.add_document_to_collection(
            'data_source_test', {"foo": 1})

        data_sources = common.get_configured_data_sources(self.accessor)
        self.assertEquals(len(data_sources), 1)
        self.assertIn('data_source_test', data_sources)
