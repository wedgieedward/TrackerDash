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

    def get_graphs(self):
        """
        return all the graph titles to display in this container
        format:
            ((<GraphName>, <bootstrapspaceing>), ..., ...)
        """
        return (("Big Graph", "col-md-8 column"), ("Small Graph", "col-md-8 column"))

    @renderer
    def graphs(self, request, tag):
        """
        """
        return Graph('test_graph_name', 400)

    @renderer
    def graphs2(self, request, tag):
        """
        """
        return Graph('test_graph_name2', 200)

    @renderer
    def anothergraph(self, request, tag):
        return Graph('another_graph', 200)

    @renderer
    def spillgraph(self, request, tag):
        """
        """
        return Graph('yes_another_graph', 200)
