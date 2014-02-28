"""
navbar element
"""

from twisted.web.template import Element, XMLFile, renderer
from twisted.python.filepath import FilePath


class NavBar(Element):
    """
    logic and rendering for the navbar
    """
    def __init__(self, dashboard):
        super(NavBar, self).__init__()
        self.loader = XMLFile(FilePath("TrackerDash/snippets/navbar.xml"))
        self.dashboard = dashboard

    def get_dashboards(self):
        """
        get all configured dashboards
        """
        return ("Dalby Dashboard", "VCS Dashboard", "Some Other Dashboard")

    @renderer
    def dashboards_dropdown(self, request, tag):
        for dashboard in self.get_dashboards():
            # TODO: make this path a variable
            dashlink = "http://localhost:8090/dash/%s" % dashboard
            yield tag.clone().fillSlots(dashName=dashboard, dashLink=dashlink)

    @renderer
    def display_link(self, request, tag):
        """
        display link header button
        """
        if self.dashboard:
            # TODO: make this path a variable
            link = "http://localhost:8090/display/%s" % self.dashboard
        else:
            link = '#'
        yield tag.clone().fillSlots(displayLink=link)
