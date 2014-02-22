"""
Template for a display page for a graph
Very similar to a dashpage without the header or footer
"""
from twisted.web.template import renderer
from dashpage import DashPage
from graphcontainer import GraphContent


class DisplayPage(DashPage):
    """
    DisplayPage object
    """
    @renderer
    def auto_refresh(self, request, tag):
        return super(DashPage, self).auto_refresh(request, tag)

    @renderer
    def content(self, request, tag):
        """
        return the content of this page
        """
        return GraphContent(self.dashboard_name)

    @renderer
    def navbar(self, request, tag):
        """
        we do not want to display the navbar
        """
        return ""

    @renderer
    def footer(self, request, tag):
        """
        we do not want to render the footer
        """
        return ""
