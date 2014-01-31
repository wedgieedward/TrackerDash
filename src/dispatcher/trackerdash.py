"""
trackerdash main application class
"""

from klein import Klein


class TrackerDash(object):
    """
    TrackerDash main object
    acts as a web server handling all the neccisary routing
    """
    app = Klein()

    def __init__(self, url='localhost', port=8089, auto_start=True):
        self._url = url
        self._port = port
        if auto_start:
            self.start_app()

    def start_app(self):
        """
        Start the klein server
        """
        self.app.run(self._url, self._port)

    @app.route('/', methods=['GET'], branch=True)
    def status(self, _request):
        """
        report the status of the application
        """
        return "Everything Is Running A-OK"
