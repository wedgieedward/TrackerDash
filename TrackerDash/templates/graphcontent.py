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

    def __init__(self, dashboard_name):
        super(GraphContent, self).__init__()
        self.loader = XMLFile(FilePath("TrackerDash/snippets/graphcontent.xml"))
        self.dashboard_name = dashboard_name
        self.accessor = MongoAccessor()
        self.dashboard_document = self.accessor.get_one_document_by_query(
            "dashboard", {"name": self.dashboard_name})
        logging.debug("Dashboard Document: %r" % self.dashboard_document)
        self._configured = True if "row_data" in self.dashboard_document else False

    @renderer
    def render_content(self, request, tag):
        """
        render the content for the graph container
        """
        if self._configured:
            graph_row_xml = XMLString(self.get_row_xml())
            return graph_row_xml.load()
        else:
            oops_container = XMLFile(FilePath("TrackerDash/snippets/no_dash_data_container.xml"))
            return oops_container.load()

    def get_row_xml(self):
        """
        """
        xml = "<div>"
        rows = self.get_rows()
        render_rows = self.get_number_of_render_rows(rows)
        for row in rows:
            xml += '<div class="row clearfix">'
            for graph_document in row:
                xml += '<div class="col-md-%s column">' % (graph_document["width"], )
                this_graph = HighchartsGraph(graph_document, render_rows)
                xml += this_graph.load()
                xml += '</div>'
            xml += '</div>'
        xml += "</div>"

        return xml

    def get_number_of_render_rows(self, rows_data):
        """
        """
        num_rows = 0
        for row in rows_data:
            row_max = 0
            for graph_document in row:
                if graph_document["height"] > row_max:
                    row_max = graph_document["height"]
            num_rows += row_max
        return num_rows

    def get_rows(self):
        """
        return all the graph titles to display in this container
        format:
        """
        return self.dashboard_document["row_data"]
