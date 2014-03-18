"""
trackerdash main application class
"""
import logging
import sys

from klein import Klein

from twisted.internet import reactor
from twisted.web.static import File

from TrackerDash.constants import APP_LOG_FILE
from TrackerDash.constants import TWISTED_LOG_FILE
from TrackerDash.templates.basewebpage import BasePage
from TrackerDash.templates.dashpage import DashPage
from TrackerDash.templates.displaypage import DisplayPage
from TrackerDash.templates.configpage import ConfigPage
from TrackerDash.templates.newdash import NewDash
from TrackerDash.templates.logpage import LogPage
from TrackerDash.database import api_request_handler as APIRequest


TWISTED_LOG = open(TWISTED_LOG_FILE, "w")


class WebDispatcher(object):
    """
    TrackerDash main object
    acts as a web server handling all the neccisary routing
    """
    app = Klein()

    def __init__(self, url, port, auto_start=True):
        self._url = url
        self._port = port
        if auto_start:
            self.start_app()

    def start_app(self):
        """
        Start the klein server
        """
        logging.info("Starting Klein App")
        self.app.run(self._url, self._port, TWISTED_LOG)

    @app.route('/', methods=['GET'])
    def index(self, _request):
        """
        Index Routing
        """
        return '<meta http-equiv="refresh" content="1;url=/dash/"/>'

    # Static files hosted on the server under web.
    # Use for static web files such as css and script files.
    @app.route('/web/', branch=True)
    def static_web_routing(self, _request):
        return File('TrackerDash/web')

    @app.route('/configure/', methods=['GET'])
    def configuration_page(self, _request):
        return ConfigPage()

    @app.route('/newdash/', methods=['GET'])
    def add_new_dashboard(self, _request):
        """
        route to new dashboard page
        """
        return NewDash()

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

    @app.route('/log/<string:log_type>', methods=["GET"])
    def get_log_page(self, _request, log_type):
        """
        return the relevant log page
        """
        if log_type == "network_log":
            return LogPage(TWISTED_LOG_FILE, "Network Log")
        elif log_type == "application_log":
            return LogPage(APP_LOG_FILE, 'TrackerDash Log')
        else:
            return LogPage

    @app.route('/shutdown/')
    def shutdown(self, _request):
        """
        TODO: put some sort of warning
        TODO: have an indicator that it has shut down
        """
        try:
            print "Closing Twisted Log File"
            TWISTED_LOG.close()
            print "Stopping Python Reactor"
            reactor.stop()
            print "Stopping Python Process"
            sys.exit("Shutting Down App")
        except SystemExit:
            # this is meant to happen, return '' so we get a 200 OK
            return ''

    # API ROUTES
    @app.route('/api/status', methods=['GET'])
    def api_status(self, _request):
        """
        route for the api to communicate with
        """
        return ''

    @app.route('/api/<string:api_request>', methods=['GET'])
    def api_get_request(self, request, api_request):
        """
        get information over the api
        """
        request_obj = APIRequest.APIGETRequest(request, api_request)
        json = request_obj.render()
        return json

    @app.route('/api/<string:api_request>', methods=['POST'])
    def api_post_request(self, request, api_request):
        """
        post information over the api
        """
        APIRequest.APIPOSTRequest(request, api_request)
        return ''
