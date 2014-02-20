"""
navbar element
"""

from twisted.web.template import Element, XMLFile, renderer
from twisted.python.filepath import FilePath


class NavBar(Element):
    """
    logic and rendering for the navbar
    """
    def __init__(self):
        super(NavBar, self).__init__()
        self.loader = XMLFile(FilePath("TrackerDash/snippets/navbar.xml"))

    def get_dashboards(self):
        """
        get all configured dashboards
        """
        return [("Dalby Dashboard", 'http://localhost:8090/dash/Dalby Dashboard'),
                ("VCS Dashboard", 'http://localhost:8090/dash/VCS Dashboard'),
                ("Some Other Dashboard", 'http://localhost:8090/dash/Some Other Dashboard')]

    @renderer
    def dashboards_dropdown(self, request, tag):
        for dashboard, link in self.get_dashboards():
            yield tag.clone().fillSlots(dashName=dashboard, dashLink=link)
