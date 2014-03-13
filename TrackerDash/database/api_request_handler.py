"""
Api request handler
"""
import json
import logging
from twisted.internet.defer import succeed
from TrackerDash.database.mongo_accessor import MongoAccessor


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


class APIGETRequest(object):

    def __init__(self, request_type):
        """
        """
        self.request_type = request_type
        self.accessor = MongoAccessor()
        self.response = self.process()

    def render(self):
        """
        """
        return json.dumps(self.response)

    def process(self):
        """
        process the request
        """
        logging.debug("Processing API Request: %s" % self.request_type)
        rt = self.request_type
        if rt == "get_dashboard_names":
            return self.get_dashboard_names()
        elif rt == "get_dashboard_information":
            return self.get_dashboard_information()
        else:
            raise NotImplementedError("request: %s is not implemented" % self.request_type)

    def get_dashboard_names(self):
        """
        return a list of dashboard names configured
        """
        dash_docs = self.accessor.get_all_documents_from_collection('dashboard')
        dashboards = [dash["name"] for dash in dash_docs]
        return {"dashboards": dashboards}

    def get_dashboard_information(self):
        """
        return the dashboard documents
        """
        dash_docs = self.accessor.get_all_documents_from_collection('dashboard')
        for doc in dash_docs:
            del doc["_id"]
        return {"dashboards": dash_docs}


class APIPOSTRequest(object):

    def __init__(self, request, request_type):
        self.request_type = request_type
        self.request = request
        self.accessor = MongoAccessor()
        self.process()

    def process(self):
        """
        """
        logging.debug("Processing API POST request: %s" % self.request_type)
        rt = self.request_type
        if rt == "post_data":
            content = json.loads(self.request.content.readlines()[0])
            data_source = content["data_source"]
            document = content["data"]
            self.accessor.add_document_to_collection_redundant(data_source, document, 60)
            return self
        else:
            raise NotImplementedError(
                "POST request: %s has not been implemented" % self.request_type)
