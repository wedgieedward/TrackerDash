"""
Dashboard Page
"""
from twisted.web.template import renderer

from basewebpage import BasePage
from navbar import NavBar
from graphcontainer import GraphContent


class DashPage(BasePage):
    auto_refresh = False
    display_alarms = False

    def __init__(self, dashboard_name):
        self.dashboard_name = dashboard_name
        super(DashPage, self).__init__()

    @renderer
    def auto_refresh(self, request, tag):
        return super(DashPage, self).auto_refresh(request, tag)

    @renderer
    def navbar(self, request, tag):
        """
        return the dashboard
        """
        return NavBar(self.dashboard_name)

    @renderer
    def content(self, request, tag):
        """
        return the content of this page
        """
        return GraphContent(self.dashboard_name)
