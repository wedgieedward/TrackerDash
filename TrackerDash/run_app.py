#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Start the server and run the app
"""
import argparse
import logging
import socket
from constants import APP_LOG_FILE
from webdispatcher import WebDispatcher

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
parser.add_argument("-p", "--port", help="run on specified port, default = 8090", type=int)


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
    args = parser.parse_args()
    host = None
    port = None
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
