"""
graph container element
"""
import logging

from twisted.web.template import Element, XMLFile, renderer, XMLString
from twisted.python.filepath import FilePath

from TrackerDash.database.mongo_accessor import MongoAccessor
from TrackerDash.templates.graph import HighchartsGraph


class DashContent(Element):
    """
    Element to handle the content of a dashboard page
    """

    def __init__(self, dashboard_name):
        super(DashContent, self).__init__()
        self.loader = XMLFile(
            FilePath("TrackerDash/snippets/graphcontent.xml"))
        self.dashboard_name = dashboard_name
        self.accessor = MongoAccessor()
        self.dashboard_document = self.accessor.get_one_document_by_query(
            "dashboard",
            {"title": self.dashboard_name})
        logging.debug("Dashboard Document: %r" % self.dashboard_document)

    @renderer
    def render_content(self, request, tag):
        """
        render the content for the graph container
        """
        try:
            graph_row_xml = XMLString(self.get_row_xml())
            return graph_row_xml.load()
        except Exception as err:
            logging.error(
                "Exception raised when rendering graphs, exception: %r" % (
                    err, ))
            oops_container = self.get_bad_container()
            return oops_container.load()

    def get_bad_container(self):
        """
        something has gone wrong that causes the page not to render correctly
        return some xml to respond to this
        """
        return XMLFile(
            FilePath("TrackerDash/snippets/no_dash_data_container.xml"))

    def get_row_xml(self):
        """
        """
        xml = "<div>"
        dashboard_row_data = self.get_dashboard_row_data()
        render_rows = self.get_number_of_render_rows(dashboard_row_data)
        for row in dashboard_row_data:
            if row is not None:
                xml += '<div class="row clearfix">'
                for dashboard_graph in row:
                    graph_document = self.accessor.get_one_document_by_query(
                        'graph', {'title': dashboard_graph["title"]})
                    if graph_document is not None:
                        xml += '<div class="col-md-%s column">' % (
                            dashboard_graph["dimensions"]["width"], )
                        this_graph = HighchartsGraph(
                            graph_document,
                            dashboard_graph["dimensions"]["height"],
                            render_rows)
                        xml += this_graph.load()
                        xml += '</div>'
                    else:
                        raise KeyError("graph not found")
                xml += '</div>'
            else:
                raise KeyError("graph not found")

        xml += "</div>"
        return xml

    def get_number_of_render_rows(self, row_data):
        """
        """
        num_rows = 0
        for row in row_data:
            if row is not None:
                row_max = 0
                for graph_document in row:
                    if graph_document is not None:
                        if graph_document["dimensions"]["height"] > row_max:
                            row_max = graph_document["dimensions"]["height"]
                num_rows += row_max
        return num_rows

    def get_dashboard_row_data(self):
        """
        return all the graph titles to display in this container
        format:
        """
        return self.dashboard_document["row_data"]
