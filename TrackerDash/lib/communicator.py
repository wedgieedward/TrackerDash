"""
TrackerDash API Library
"""
import json
import requests
import urllib2


class Communicator(object):
    """
    Communicator Class To TrackerDash
    Provides a scriptable interface to TrackerDash Library
    """
    post_header = {'Content-type': 'application/json', 'Accept': 'text/plain'}

    def __init__(self, host, port):
        self._host = host
        self._port = port
        self._url = "http://%s:%s" % (self._host, self._port)

    def _test_connection(self):
        """
        tests that we can communicate with a TrackerDash instance
        """
        try:
            socket = urllib2.urlopen(self._url + '/api/status')
            code = socket.getcode()
            if code == 200:
                return (True, "Connection Successful")
            else:
                return (False, "Returned %s error" % code)

        except urllib2.HTTPError:
            return (False, "Could not connect to server")

        except urllib2.URLError:
            return (False, "Connection Refused")

    def get_dashboard_names(self):
        """
        return a list of configured dashboards
        """
        try:
            data = json.load(urllib2.urlopen(self._url + '/api/get_dashboard_names'))
            return data["dashboards"]

        except Exception as exc:
            return exc

    def get_dashboard_information(self, dashboard_name=False):
        """
        given a dashboard name, get it's information
        """
        try:
            data = json.load(urllib2.urlopen(self._url + '/api/get_dashboard_information'))
            if dashboard_name:
                dashboard_info = []
                for dash in data["dashboards"]:
                    if dash["name"] == dashboard_name:
                        dashboard_info = dash
                        break
            else:
                return data["dashboards"]

            return dashboard_info

        except Exception as exc:
            return exc

    def post_data_to_data_source(self, data_source, data):
        """
        given a data_source, add data to it
        """
        json_data = json.dumps({"data_source": data_source, "data": data})
        return requests.post(self._url + 'api/post_data', data=json_data, headers=self.post_header)
