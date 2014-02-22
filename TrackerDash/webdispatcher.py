"""
trackerdash main application class
"""
import logging
from klein import Klein
from twisted.web.static import File

from templates.basewebpage import BasePage
from templates.dashpage import DashPage
from templates.displaypage import DisplayPage
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
        return '<meta http-equiv="refresh" content="1;url=http://localhost:8090/dash/"/>'

    # Static files hosted on the server under web.
    # Use for static web files such as css and script files.
    @app.route('/web/', branch=True)
    def static_web_routing(self, _request):
        return File('TrackerDash/web')

    # Temp route to the graphing library. This should be removed
    # once graphing has been implemented.
    @app.route('/graph/', branch=True)
    def third_party_graphs(self, _request):
        """
        test route link to view the contents of thirdparty
        """
        return File('TrackerDash/thirdparty')

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
    def basedash(self, _request):
        """
        route to the test html page
        """
        return BasePage()

    @app.route('/dash/<string:dashboard>', methods=["GET"])
    def get_dash_page(self, _request, dashboard):
        """
        dynamically route to a specific dashboard page
        """
        return DashPage(dashboard)

    @app.route('/display/<string:dashboard>', methods=["GET"])
    def get_display_page(self, _request, dashboard):
        """
        return a displaypage
        """
        return DisplayPage(dashboard)
