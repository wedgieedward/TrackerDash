"""
trackerdash main application class
"""
import logging
from klein import Klein
from twisted.web.static import File
from pprint import pprint

from TrackerDash.templates.welcomepage import WelcomePage


class WebDispatcher(object):
    """
    TrackerDash main object
    acts as a web server handling all the neccisary routing
    """
    app = Klein()

    def __init__(self, url, port, auto_start=True):
        logging.info("WebDispatcher instance is being created")
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
    def welcome_page(self, _request):
        """
        Bring up the welcome page
        """
        return self.get_page('TrackerDash/web/welcome_page.html')

    @app.route('/web/', branch=True)
    def static_web_routing(self, _request):
        return File('TrackerDash/web')

    @app.route('/status/', methods=['GET'])
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

    def get_page(self, path):
        """
        very cheap way of getting the static file
        TODO: find a more twisted/twisted-klein way of doing this.
        """
        a = open(path, 'r')
        string = ''.join(a.readlines())
        return string

