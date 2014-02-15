"""
base web page
"""
import logging
from twisted.web.template import Element, XMLFile, renderer, TagLoader, flattenString, XMLString
from twisted.python.filepath import FilePath


class BasePage(Element):
    """
    Object for base webpage
    """
    def __init__(self, dashboard=''):
        super(BasePage, self).__init__()
        self.loader = XMLFile(FilePath("TrackerDash/pages/basewebpage.html"))

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

    @renderer
    def page_content(self, request, tag):
        """
        renderer for the main page content
        """


