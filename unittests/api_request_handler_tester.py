"""
tests the behaviour of the API request handler
"""
import unittest
from TrackerDash.database import api_request_handler
from TrackerDash.database.mongo_accessor import TestAccessor


class MockRequest(object):
    """
    mock twisted http request
    """
    def __init__(self, content):
        self.content = content

    def get_content(self):
        """
        overriden function to get content from the "request"
        """
        return self.content


class MockAPIGetRequest(api_request_handler.APIGETRequest):

    def __init__(self, request, request_type):
        self.accessor = TestAccessor()
        self.request = request
        self.request_type = request_type
        # no process


class TestAPIGETReqest(unittest.TestCase):
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
            request_handler = MockAPIGetRequest(MockRequest({}), request_type)
            request_handler.process()

    def test_get_dashboard_names(self):
        """
        tests get_dashboard_names
        """
        request_handler = MockAPIGetRequest(MockRequest({}), '')
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
        request_handler = MockAPIGetRequest(MockRequest({}), '')
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
        request_handler = MockAPIGetRequest(MockRequest({}), '')
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
        request_handler = MockAPIGetRequest(MockRequest({}), '')
        dash_names = request_handler.get_graph_information()
        self.assertIn('graphs', dash_names)
        self.assertEquals(len(dash_names["graphs"]), 0)

        self.accessor.add_document_to_collection(
            'graph', {"title": 'hello'})
        dash_names = request_handler.get_graph_information()
        self.assertIn('graphs', dash_names)
        self.assertEquals(len(dash_names["graphs"]), 1)
        self.assertEquals(dash_names["graphs"][0]["title"], 'hello')

