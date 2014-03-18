"""
navbar element
"""
from twisted.web.template import Element, XMLFile, renderer
from twisted.python.filepath import FilePath

from TrackerDash.database import common
from TrackerDash.database.mongo_accessor import MongoAccessor
from TrackerDash.constants import VERSION, TAG


class NavBar(Element):
    """
    logic and rendering for the navbar
    """
    def __init__(self, dashboard):
        super(NavBar, self).__init__()
        self.loader = XMLFile(FilePath("TrackerDash/snippets/navbar.xml"))
        self.dashboard = dashboard
        self.accessor = MongoAccessor()

    @renderer
    def software_version(self, request, tag):
        """
        get the software_version
        """
        return TAG + ' ' + VERSION

    @renderer
    def dashboards_dropdown(self, request, tag):
        dashboards = common.get_dashboard_names(self.accessor)
        for dashboard in dashboards:
            dashlink = "../dash/%s" % dashboard
            yield tag.clone().fillSlots(dashName=dashboard, dashLink=dashlink)

    @renderer
    def display_link(self, request, tag):
        """
        display link header button
        """
        if self.dashboard:
            link = "../display/%s" % self.dashboard
        else:
            link = '#'
        yield tag.clone().fillSlots(displayLink=link)
