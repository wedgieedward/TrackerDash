"""
Template for a display page for a graph
Very similar to a dashpage without the header or footer
"""
from twisted.python.filepath import FilePath
from twisted.web.template import renderer, XMLString, XMLFile

from dashpage import DashPage
from graphcontainer import GraphContent


class DisplayPage(DashPage):
    """
    DisplayPage object
    """
    refresh_interval = 60

    @renderer
    def auto_refresh(self, request, tag):
        return XMLString(
            '<meta http-equiv="refresh" content="%s"></meta>' % (self.refresh_interval)).load()

    @renderer
    def header_scripts(self, request, tag):
        """
        return the header script tags required for this page
        """
        return XMLFile(FilePath("TrackerDash/snippets/headerscripts.xml")).load()

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
