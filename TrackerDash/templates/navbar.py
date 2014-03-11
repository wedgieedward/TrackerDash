"""
navbar element
"""
import unittest

from twisted.web.template import Element, XMLFile, renderer
from twisted.python.filepath import FilePath

from TrackerDash.database.mongo_accessor import MongoAccessor, TestAccessor


class NavBar(Element):
    """
    logic and rendering for the navbar
    """
    def __init__(self, dashboard):
        super(NavBar, self).__init__()
        self.loader = XMLFile(FilePath("TrackerDash/snippets/navbar.xml"))
        self.dashboard = dashboard
        self.accessor = MongoAccessor()

    def get_dashboards(self):
        """
        get all configured dashboards
        """
        dash_documents = self.accessor.get_all_documents_from_collection("dashboard")
        dash_names = [dash["name"] for dash in dash_documents]
        return dash_names

    @renderer
    def dashboards_dropdown(self, request, tag):
        for dashboard in self.get_dashboards():
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
