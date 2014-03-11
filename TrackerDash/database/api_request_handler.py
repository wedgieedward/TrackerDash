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

    if arguments.keys()[0] == "create_dashboard":
        return create_dashboard_request_handler(arguments["create_dashboard"])


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
