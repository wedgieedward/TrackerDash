"""
Dashboard Page
"""
from twisted.python.filepath import FilePath
from twisted.web.template import renderer, XMLFile

from TrackerDash.templates.basewebpage import BasePage
from TrackerDash.templates.navbar import NavBar
from TrackerDash.templates.dashcontent import DashContent


class DashPage(BasePage):
    display_alarms = False

    def __init__(self, dashboard_name):
        self.dashboard_name = dashboard_name
        super(DashPage, self).__init__()

    @renderer
    def auto_refresh(self, request, tag):
        return ''

    @renderer
    def navbar(self, request, tag):
        """
        return the dashboard
        """
        return NavBar(self.dashboard_name, 'dashboard')

    @renderer
    def header_scripts(self, request, tag):
        """
        return the header script tags required for this page
        """
        return XMLFile(
            FilePath("TrackerDash/snippets/dashheaderscripts.xml")).load()

    @renderer
    def content(self, request, tag):
        """
        return the content of this page
        """
        return DashContent(self.dashboard_name)
