"""
Api request handler
"""
import json
import logging
from twisted.internet.defer import succeed

from TrackerDash.common import theme_helpers
from TrackerDash.database import common as db_common
from TrackerDash.database.mongo_accessor import MongoAccessor
from TrackerDash.schemas.api import Graph as GraphSchema
from TrackerDash.schemas.api import Dashboard as DashboardSchema


def process_request(request):
    """
    Given a request, do stuff.
    """
    arguments = request.args
    if len(arguments.keys()) != 1:
        raise SyntaxError("Too many arguments")

    method = arguments.keys()[0]
    if method == "create_dashboard":
        return create_dashboard_request_handler(arguments["create_dashboard"])
    else:
        raise NotImplementedError("No API method for request type '%s'" % method)


def create_dashboard_request_handler(data):
    """
    """
    logging.info("create_dashboard_request_handler: data=%r" % data)
    dashboard_name = json.loads(data[0])["name"]
    accessor = MongoAccessor()
    docs = accessor.get_documents_by_query("dashboard", {"name": dashboard_name})
    if docs == []:
        accessor.add_document_to_collection("dashboard", {"name": dashboard_name})
    else:
        raise NameError("Document Already Exists")
    return succeed


class APIRequest(object):
    """
    Base class for an API request
    """

    def __init__(self, request, request_type):
        self.accessor = MongoAccessor()
        self.request = request
        self.request_type = request_type
        self.process()

    def process(self):
        """
        Needs to be overridden
        """
        raise NotImplementedError


class APIGETRequest(APIRequest):

    def __init__(self, request, request_type):
        """
        """
        self.response = None
        super(APIGETRequest, self).__init__(request, request_type)

    def render(self):
        """
        """
        return json.dumps(self.response)

    def process(self):
        """
        process the request
        should not return anything
        raise exceptions here to generate a http 500 error
        """
        logging.debug("Processing API Request: %s" % self.request_type)
        rt = self.request_type
        if rt == "get_dashboard_names":
            self.response = self.get_dashboard_names()
        elif rt == "get_dashboard_information":
            self.response = self.get_dashboard_information()
        elif rt == "get_graph_names":
            self.response = self.get_graph_names()
        elif rt == "get_graph_information":
            self.response = self.get_graph_information()
        elif rt == "get_data_sources":
            self.response = {"data_sources": db_common.get_configured_data_sources(self.accessor)}
        else:
            logging.info("request: %s is not implemented" % self.request_type)
            raise NotImplementedError("request: %s is not implemented" % self.request_type)

    def get_dashboard_names(self):
        """
        return a list of dashboard names configured
        """
        return {"dashboards": db_common.get_dashboard_names(self.accessor)}

    def get_dashboard_information(self):
        """
        return the dashboard documents
        """
        dash_docs = self.accessor.get_all_documents_from_collection('dashboard')
        for doc in dash_docs:
            del doc["_id"]
        return {"dashboards": dash_docs}

    def get_graph_information(self):
        """
        get all the configured graph information
        """
        graph_docs = self.accessor.get_all_documents_from_collection('graph')
        for doc in graph_docs:
            del doc["_id"]
        return {"graphs": graph_docs}

    def get_graph_names(self):
        """
        get the names of all the configured graphs
        """
        graph_docs = self.get_graph_information()
        graph_names = [graph["title"] for graph in graph_docs["graphs"]]
        return {"graphs": graph_names}


class APIPOSTRequest(APIRequest):

    def __init__(self, request, request_type):
        super(APIPOSTRequest, self).__init__(request, request_type)

    def process(self):
        """
        """
        logging.debug("Processing API POST request: %s" % self.request_type)
        rt = self.request_type
        content = json.loads(self.request.content.readlines()[0])

        # Post Raw Data To A Data Source
        if rt == "post_data":
            data_source = content["data_source"]
            document = content["data"]
            # No validation needed here as we can post to a non existant data source
            self.accessor.add_document_to_collection_redundant(data_source, document, 60)
            return self

        # Create a new graph object
        elif rt == "create_graph":
            graph_data = content["data"]
            schema = GraphSchema()
            graph_data_validated = schema.deserialize(graph_data)

            # We need to ensure that a datasource collection is present.
            try:
                self.accessor.create_collection(graph_data_validated["data_source"])
            except NameError:
                logging.debug(
                    "data source for graph '%s' already exists" % graph_data_validated["title"])
            self.accessor.add_document_to_collection("graph", graph_data_validated)
            return self

        # Create a new dashboard
        elif rt == "create_dashboard":
            dashboard_data = content["data"]
            logging.info("create_dashboard request data: %r" % dashboard_data)
            schema = DashboardSchema()
            dashboard_data_validated = schema.deserialize(dashboard_data)
            self.accessor.add_document_to_collection("dashboard", dashboard_data_validated)

        elif rt == "set_theme":
            logging.info("content for set_theme: %r" % content)
            theme_helpers.set_theme(self.accessor, content)
            return self

        elif rt == "set_style":
            logging.info("content for set_style: %r" % content)
            theme_helpers.set_style(self.accessor, content)
            return self

        else:
            logging.info("request: %s is not implemented" % self.request_type)
            raise NotImplementedError(
                "POST request: %s has not been implemented" % self.request_type)
