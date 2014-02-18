"""
trackerdash main application class
"""
import logging
from klein import Klein
from twisted.web.static import File

from templates.basewebpage import BasePage
from templates.configpage import ConfigPage


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
    def index(self, _request):
        """
        Index Routing
        """
        start_page = '/web/welcome_page.html'
        return '<meta http-equiv="refresh" content="0; url=%s" />' % start_page

    @app.route('/web/', branch=True)
    def static_web_routing(self, _request):
        return File('TrackerDash/web')

    @app.route('/graph/', branch=True)
    def third_party_graphs(self, _request):
        """
        test route link to view the contents of thirdparty
        """
        return File('TrackerDash/thirdparty')

    @app.route('/status/', methods=['GET'])
    def status(self, _request):
        """
        report the status of the application
        note:: not currently implemented, placeholder for status
        """
        logging.info("Request at path '/'")
        return "Everything Is Running A-OK"

    @app.route('/configure/', methods=['GET'])
    def configuration_page(self, _request):
        return ConfigPage()

    @app.route('/api/', methods=['POST'])
    def api(self, request):
        """
        post to the database over the api

        note:: not currently implemented, placeholder for api
        """
        logging.info("Request at path '/api/")
        arguments = request.args.get()
        return arguments

    @app.route('/dash/', methods=["GET"])
    def testpage(self, _request):
        """
        route to the test html page
        """
        return BasePage()

    @app.route('/dash/<string:dashboard>', methods=["GET"])
    def get_dash_page(self, _request, dashboard=''):
        """
        dynamically route to a specific dashboard page
        """
        return BasePage(dashboard)
