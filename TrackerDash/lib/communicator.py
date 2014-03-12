"""
TrackerDash API Library
"""
import urllib2


class Communicator(object):
    """
    Communicator Class To TrackerDash
    Provides a scriptable interface to TrackerDash Library
    """

    def __init__(self, host, port):
        self._host = host
        self._port = port
        self._url = "http://%s:%s" % (self._host, self._port)

    def _test_connection(self):
        """
        tests that we can communicate with a TrackerDash instance
        """
        try:
            socket = urllib2.urlopen(self._url + '/status/api')
            code = socket.getcode()
            if code == 200:
                return (True, "Connection Successful")
            else:
                return (False, "Returned %s error" % code)

        except urllib2.HTTPError:
            return (False, "Could not connect to server")

        except urllib2.URLError:
            return (False, "Connection Refused")
