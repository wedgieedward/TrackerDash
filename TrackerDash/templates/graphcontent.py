"""
graph container element
"""
import logging

from twisted.web.template import Element, XMLFile, renderer, XMLString
from twisted.python.filepath import FilePath

from TrackerDash.database.mongo_accessor import MongoAccessor
from TrackerDash.templates.graph import HighchartsGraph


class GraphContent(Element):
    """
    Element to handle the content of a dashboard page
    """

    def __init__(self, graph_name):
        super(GraphContent, self).__init__()
        self.loader = XMLFile(
            FilePath("TrackerDash/snippets/graphcontent.xml"))
        self.graph_name = graph_name
        self.accessor = MongoAccessor()
        self.graph_document = self.accessor.get_one_document_by_query(
            "graph",
            {"title": self.graph_name})
        logging.debug("Graph Document: %r" % self.graph_document)

    @renderer
    def render_content(self, request, tag):
        """
        render the content for the graph container
        """
        if self.graph_document is not None:
            graph_row_xml = XMLString(self.get_graph_xml())
            return graph_row_xml.load()
        else:
            oops_container = self.get_bad_container()
            return oops_container.load()

    def get_bad_container(self):
        """
        something has gone wrong that causes the page not to render correctly
        return some xml to respond to this
        """
        return XMLFile(
            FilePath("TrackerDash/snippets/no_dash_data_container.xml"))

    def get_graph_xml(self):
        """
        """
        xml = "<div>"
        xml += '<div class="row clearfix">'
        xml += '<div class="col-md-12 column">'
        this_graph = HighchartsGraph(self.graph_document, 1, 1)
        xml += this_graph.load()
        xml += '</div>'
        xml += '</div>'
        xml += "</div>"

        return xml
