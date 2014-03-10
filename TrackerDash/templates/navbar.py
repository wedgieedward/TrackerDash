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


class NavBarSanity(unittest.TestCase):
    """
    """
    def setUp(self):
        self.nav_bar = NavBar(None)
        self.test_accessor = TestAccessor()
        self.nav_bar.accessor = self.test_accessor
        self.test_accessor.reset_all()

    def test_get_dash_names(self):
        """
        tests that the object inheretance works as expected
        """
        dashboards = self.nav_bar.get_dashboards()
        self.assertEquals(len(dashboards), 0)
        test_dash_name = "test-dash-name"
        self.test_accessor.add_document_to_collection("dashboard", {"name": test_dash_name})

        dashboards = self.nav_bar.get_dashboards()
        self.assertEquals(len(dashboards), 1)
        self.assertIn(test_dash_name, dashboards)


if __name__ == '__main__':
    unittest.main()
