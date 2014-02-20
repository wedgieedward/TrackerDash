"""
Dashboard Page
"""
from twisted.web.template import renderer

from basewebpage import BasePage
from graphcontainer import GraphContent


class DashPage(BasePage):
    auto_refresh = True
    display_alarms = False

    def __init__(self, dashboard_name):
        self.dashboard_name = dashboard_name
        super(DashPage, self).__init__()

    @renderer
    def auto_refresh(self, request, tag):
        return super(DashPage, self).auto_refresh(request, tag)

    @renderer
    def content(self, request, tag):
        """
        return the content of this page
        """
        return GraphContent(self.dashboard_name)
