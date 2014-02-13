#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Start the server and run the app
"""
import logging
from trackerdash import TrackerDash

URL = 'localhost'
PORT = 8090

if __name__ == '__main__':
    logging.info("Starting TrackerDash")
    app = TrackerDash(URL, PORT)
