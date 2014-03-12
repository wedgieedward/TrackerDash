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
