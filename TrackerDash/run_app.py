#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Start the server and run the app
TODO: Add argument parsing
"""
import logging
from webdispatcher import WebDispatcher

URL = 'localhost'
PORT = 8090

if __name__ == '__main__':
    logging.info("Starting TrackerDash")
    app = WebDispatcher(URL, PORT)
