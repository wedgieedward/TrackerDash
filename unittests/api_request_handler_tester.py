"""
tests the behaviour of the API request handler
"""
import unittest

from TrackerDash.database import api_request_handler
from TrackerDash.database import demo_data
from TrackerDash.database.mongo_accessor import TestAccessor


class MockAPIGetRequest(api_request_handler.APIGETRequest):

    def __init__(self, request_type):
        self.accessor = TestAccessor()
        self.request_type = request_type
        # no process


class MockAPIPostRequest(api_request_handler.APIPOSTRequest):

    def __init__(self, request_type, request_content):
        self.accessor = TestAccessor()
        self.request_type = request_type
        self.content = request_content
        # no process

    def get_content(self):
        """
        overriden function to get content from the "request"
        """
        return {"data": self.content}


class TestAPIGETRequest(unittest.TestCase):
    """
    unit tests for the APIGETRequest
    """
    accessor = TestAccessor()
    known_requests = (
        "get_dashboard_names",
        "get_dashboard_information",
        "get_graph_names",
        "get_graph_information",
        "get_data_sources"
    )

    def setUp(self):
        """
        set up test cases for unittesting
        """
        self.accessor.reset_all()

    def test_known_request_types(self):
        """
        tests that the known requests do not raise an error
        """
        for request_type in self.known_requests:
            request_handler = MockAPIGetRequest(request_type)
            request_handler.process()

    def test_unknown_request_type(self):
        """
        tests that we do blow up correctly if we do have a bad request type
        """
        request_handler = MockAPIGetRequest('bad_request')
        self.assertRaises(NotImplementedError, request_handler.process)

    def test_get_dashboard_names(self):
        """
        tests get_dashboard_names
        """
        request_handler = MockAPIGetRequest('')
        dash_names = request_handler.get_dashboard_names()
        self.assertIn('dashboards', dash_names)
        self.assertEquals(len(dash_names["dashboards"]), 0)

        self.accessor.add_document_to_collection(
            'dashboard', {"title": 'hello'})
        dash_names = request_handler.get_dashboard_names()
        self.assertIn('dashboards', dash_names)
        self.assertEquals(len(dash_names["dashboards"]), 1)
        self.assertEquals(dash_names["dashboards"][0], 'hello')

    def test_get_dashboard_information(self):
        """
        tests get_dashboard_information
        """
        request_handler = MockAPIGetRequest('')
        dash_names = request_handler.get_dashboard_information()
        self.assertIn('dashboards', dash_names)
        self.assertEquals(len(dash_names["dashboards"]), 0)

        self.accessor.add_document_to_collection(
            'dashboard', {"title": 'hello'})
        dash_names = request_handler.get_dashboard_information()
        self.assertIn('dashboards', dash_names)
        self.assertEquals(len(dash_names["dashboards"]), 1)
        self.assertEquals(dash_names["dashboards"][0]["title"], 'hello')

    def test_get_graph_names(self):
        """
        tests get_graph_names
        """
        request_handler = MockAPIGetRequest('')
        dash_names = request_handler.get_graph_names()
        self.assertIn('graphs', dash_names)
        self.assertEquals(len(dash_names["graphs"]), 0)

        self.accessor.add_document_to_collection(
            'graph', {"title": 'hello'})
        dash_names = request_handler.get_graph_names()
        self.assertIn('graphs', dash_names)
        self.assertEquals(len(dash_names["graphs"]), 1)
        self.assertEquals(dash_names["graphs"][0], 'hello')

    def test_get_graph_information(self):
        """
        tests get_graph_information
        """
        request_handler = MockAPIGetRequest('')
        dash_names = request_handler.get_graph_information()
        self.assertIn('graphs', dash_names)
        self.assertEquals(len(dash_names["graphs"]), 0)

        self.accessor.add_document_to_collection(
            'graph', {"title": 'hello'})
        dash_names = request_handler.get_graph_information()
        self.assertIn('graphs', dash_names)
        self.assertEquals(len(dash_names["graphs"]), 1)
        self.assertEquals(dash_names["graphs"][0]["title"], 'hello')


class TestAPIPOSTRequest(unittest.TestCase):
    """
    test APIPOSTRequest
    """

    def test_unknown_request_type(self):
        """
        tests that we do blow up correctly if we do have a bad request type
        """
        request_handler = MockAPIPostRequest('bad_request', {})
        self.assertRaises(NotImplementedError, request_handler.process)

    def _map_content_by_collection(self, collection):
        """
        lazy method to test post requests are valid given a collection name
        """
        mapping = {
            'graph': 'create_graph',
            'dashboard': 'create_dashboard',
            'named_data_source': 'post_data'
        }
        return mapping[collection]

    def _test_api_post_requests(self):
        """
        lazy method to test all requests
        """
        for collection, document in demo_data.DEMO_DATA:
            request_type = self._map_content_by_collection(collection)
