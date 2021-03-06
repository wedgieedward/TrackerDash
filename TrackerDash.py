#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Start the server and run the app
"""
import argparse
import logging
import logging.handlers
import socket
import sys
from TrackerDash.constants import APP_LOG_FILE
from TrackerDash.database import common as database_common
from TrackerDash.database.mongo_accessor import MongoAccessor
from TrackerDash.webdispatcher import WebDispatcher

# logging setup
logging.basicConfig(filename=APP_LOG_FILE, filemode='w', level=logging.INFO)
logging.info("Initialised Log File")

# defaults
localhost = 'localhost'
defaultport = 8090

parser = argparse.ArgumentParser()
parser.add_argument(
    "-l",
    "--local",
    help="run app on localhost, default = local ip address",
    action="store_true")
parser.add_argument(
    "-c",
    "--clean",
    help="WARNING: clears the entire database back to base settings",
    action="store_true")
parser.add_argument(
    "-sc",
    "--safe_clean",
    help="Remove all database configuration except data_sources",
    action="store_true")
parser.add_argument(
    "-cd",
    "--clean_datasources",
    help="WARNING: clears all the data sources in the database",
    action="store_true")
parser.add_argument(
    "-d",
    "--demo_data",
    help="Add mock demo data to the database",
    action="store_true")
parser.add_argument(
    "-p",
    "--port",
    help="run on specified port, default = 8090",
    type=int)


def get_ip_address():
    """
    get the ip address of this system
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect(("google.com", 80))
    ip_addr = sock.getsockname()[0]
    sock.close()
    return ip_addr


if __name__ == '__main__':
    logging.info("Starting TrackerDash")
    if not database_common.is_mongo_running():
        print ("Could not connect to a running mongodb instance"
               "please run 'sudo service mongodb start'")
        sys.exit()
    print "Found mongodb instance running"

    accessor = MongoAccessor()
    if not database_common.is_mongo_configured(accessor):
        print "Database not configured to run TrackerDash, initialising now."
        logging.debug(
            "database is not configured, adding essential collections")
        accessor.add_essential_collections()

    args = parser.parse_args()
    host = None
    port = None
    if args.clean:
        for x in range(5):
            # Only want to prompt up to 5 times
            user_input = raw_input(
                "WARNING: Are You Sure You Want To Clear The Database? "
                "[y|N] default: no: ")
            if user_input in ('y', 'Y'):
                print "Clearing the database."
                accessor.reset_all()
                break
            elif user_input in ('', 'n', 'N'):
                print "Not clearing the database."
                break
    if args.clean_datasources:
        print "Cleaning Datasources"
        for collection in database_common.get_configured_data_sources(
                accessor):
            accessor.delete_collection(collection)
    if args.safe_clean:
        print "Cleaning out Essential Collections, preserving datasources"
        accessor.reset_essential_collections()
    if args.demo_data:
        print "Adding demo data to the database."
        database_common.add_demo_data(accessor)

    if args.local:
        host = localhost
    else:
        host = get_ip_address()

    if args.port:
        port = args.port
    else:
        port = defaultport
    logging.debug("Running on %s:%s" % (host, port))
    # Leaving this in to indicate that it is running
    # having a clickable url in the terminal aids ease of use
    print "Started on: http://%s:%s" % (host, port)
    app = WebDispatcher(host, port)
