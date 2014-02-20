"""
graph container element
"""
from twisted.web.template import Element, XMLFile, renderer
from twisted.python.filepath import FilePath

from graph import Graph


class GraphContent(Element):
    """
    Element to handle the content of a dashboard page
    """

    def __init__(self, dashboard):
        super(GraphContent, self).__init__()
        self.loader = XMLFile(FilePath("TrackerDash/snippets/graphcontainer.xml"))
        self.dashboard = dashboard

    @renderer
    def dashname(self, request, tag):
        """
        return the dashname
        """
        return self.dashboard

    @renderer
    def graphs(self, request, tag):
        """
        """
        return Graph('test_graph_name')
