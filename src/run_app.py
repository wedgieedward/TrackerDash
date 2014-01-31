#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Start the server and run the app
"""
from trackerdash import TrackerDash


if __name__ == '__main__':
    app = TrackerDash('localhost', 8090)
