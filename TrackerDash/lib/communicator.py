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
    _post_header = {'Content-type': 'application/json', 'Accept': 'text/plain'}

    def __init__(self, host, port):
        self._host = host
        self._port = port
        self._url = "http://%s:%s" % (self._host, self._port)

    def create_new_dashboard(self, dashboard_data):
        """
        given a dictionary containing the data for a dashboard create a dashboard
        dashboard_data:
            name (type: string, unique: True)
            row_data (array of rows)

        row:
            an array of strings that map to a configured graph
        """
        json_data = json.dumps({"data": dashboard_data})
        return requests.post(
            self._url + '/api/create_dashboard',
            data=json_data,
            headers=self._post_header)

    def create_new_graph(self, graph_data):
        """
        given a dictionary containing the data for a graph create a new graph
        """
        json_data = json.dumps({"data": graph_data})
        return requests.post(
            self._url + '/api/create_graph',
            data=json_data,
            headers=self._post_header)

    def get_dashboard_information(self, dashboard_name=False):
        """
        given a dashboard name, get it's information
        """
        data = json.load(urllib2.urlopen(
            self._url + '/api/get_dashboard_information'))
        if dashboard_name:
            dashboard_info = []
            for dash in data["dashboards"]:
                if dash["name"] == dashboard_name:
                    dashboard_info = dash
                    break
        else:
            return data["dashboards"]

        return dashboard_info

    def get_dashboard_names(self):
        """
        return a list of configured dashboards
        """
        data = json.load(
            urllib2.urlopen(self._url + '/api/get_dashboard_names'))
        return data["dashboards"]

    def get_data_sources(self):
        """
        get all the configured data_sources
        """
        data = json.load(
            urllib2.urlopen(self._url + '/api/get_data_sources'))
        return data["data_sources"]

    def get_graph_information(self, graph_name=None):
        """
        get all the configured graphs unless a specific graph name is specified
        if graph_name is specified return just that graph's information
        """
        data = json.load(
            urllib2.urlopen(self._url + '/api/get_graph_information'))
        if graph_name:
            graph_info = []
            for graph in data["graphs"]:
                if graph["title"] == graph_name:
                    graph_info = graph
                    break
        else:
            return data["graphs"]

        return graph_info

    def get_graph_names(self):
        """
        get a list of names for configured graphs
        """
        data = json.load(urllib2.urlopen(self._url + '/api/get_graph_names'))
        return data["graphs"]

    def post_data_to_data_source(self, data_source, data):
        """
        given a data_source, add data to it
        """
        json_data = json.dumps({"data_source": data_source, "data": data})
        return requests.post(
            self._url + '/api/post_data',
            data=json_data,
            headers=self._post_header)

    def test_connection(self):
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
