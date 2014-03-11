"""
trackerdash main application class
"""
import logging
import sys

from klein import Klein

from twisted.internet import reactor
from twisted.internet.defer import succeed
from twisted.web.static import File

from constants import APP_LOG_FILE
from constants import TWISTED_LOG_FILE
from templates.basewebpage import BasePage
from templates.dashpage import DashPage
from templates.displaypage import DisplayPage
from templates.configpage import ConfigPage
from templates.newdash import NewDash
from templates.logpage import LogPage


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
        logging.info("Request at \'/\'")
        return '<meta http-equiv="refresh" content="1;url=/dash/"/>'

    # Static files hosted on the server under web.
    # Use for static web files such as css and script files.
    @app.route('/web/', branch=True)
    def static_web_routing(self, _request):
        logging.info("Request at \'/web/\'")
        return File('TrackerDash/web')

    @app.route('/configure/', methods=['GET'])
    def configuration_page(self, _request):
        logging.info("Request at \'/configure/\'")
        return ConfigPage()

    @app.route('/newdash/', methods=['GET'])
    def add_new_dashboard(self, _request):
        """
        route to new dashboard page
        """
        logging.info("Request at \'/newdash/\'")
        return NewDash()

    @app.route('/api/', methods=['POST'])
    def api(self, request):
        """
        post to the database over the api
        note:: not currently implemented, placeholder for api
        """
        logging.info("Request at \'/api/\'")
        return succeed(None)

    @app.route('/dash/', methods=["GET"])
    def basedash(self, _request):
        """
        route to the test html page
        """
        logging.info("Request at \'/dash/\'")
        return BasePage()

    @app.route('/dash/<string:dashboard>', methods=["GET"])
    def get_dash_page(self, _request, dashboard):
        """
        dynamically route to a specific dashboard page
        """
        logging.info("Request at \'/dash/%s\'" % dashboard)
        return DashPage(dashboard)

    @app.route('/display/<string:dashboard>', methods=["GET"])
    def get_display_page(self, _request, dashboard):
        """
        return a displaypage
        """
        logging.info("Request at \'/display/%s\'" % dashboard)
        return DisplayPage(dashboard)

    @app.route('/log/<string:log_type>', methods=["GET"])
    def get_log_page(self, _request, log_type):
        """
        return the relevant log page
        """
        logging.info("Request at \'/log/%s\'" % log_type)
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
