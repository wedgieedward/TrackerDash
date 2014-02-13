"""
trackerdash main application class
"""
import logging
from klein import Klein
from basewebpage import BaseWebPage


class TrackerDash(object):
    """
    TrackerDash main object
    acts as a web server handling all the neccisary routing
    """
    app = Klein()

    def __init__(self, url='localhost', port=8089, auto_start=True):
        logging.info("TrackerDash instance is being created")
        self._url = url
        self._port = port
        if auto_start:
            self.start_app()

    def start_app(self):
        """
        Start the klein server
        """
        logging.info("Running start app")
        self.app.run(self._url, self._port)

    @app.route('/', methods=['GET'])
    def status(self, _request):
        """
        report the status of the application
        """
        logging.info("Request at path '/'")
        return "Everything Is Running A-OK"

    @app.route('/api/', methods=['POST'])
    def api(self, request):
        """
        post to the database over the api
        """
        logging.info("Request at path '/api/")
        arguments = request.args.get()
        return arguments

    @app.route('/test/base/', methods=["GET"])
    def testpage(self, _request):
        """
        route to the test html page
        """
        logging.info("Request at path '/test/base/")
        return BaseWebPage('pages/basepage.html')
