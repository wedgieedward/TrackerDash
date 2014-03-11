"""
graph container element
"""
import uuid

from twisted.web.template import Element, XMLFile, renderer, XMLString
from twisted.python.filepath import FilePath

from graph import Graph


class GraphContent(Element):
    """
    Element to handle the content of a dashboard page
    """

    def __init__(self, dashboard_name):
        super(GraphContent, self).__init__()
        self.loader = XMLFile(FilePath("TrackerDash/snippets/graphcontent.xml"))
        self.dashboard_name = dashboard_name

    @renderer
    def render_content(self, request, tag):
        """
        render the content for the graph container
        """
        graph_row_xml = XMLString(self.get_row_xml())
        return graph_row_xml.load()

    def get_row_xml(self):
        """
        """
        xml = "<div>"
        rows = self.get_rows()
        render_rows = self.get_number_of_render_rows(rows)
        for row in rows:
            xml += '<div class="row clearfix">'
            for graph in row:
                xml += '<div class="col-md-%s column">' % (graph["width"], )
                this_graph = Graph(
                    graph["name"],
                    graph["description"],
                    graph["data_source"],
                    graph["height"],
                    render_rows)
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
            for graph in row:
                if graph["height"] > row_max:
                    row_max = graph["height"]
            num_rows += row_max
        return num_rows

    def get_rows(self):
        """
        return all the graph titles to display in this container
        format:
        """
        desc = "Randomly generated data for test purposes"
        return [
            [{"name": "Big Graph",
              "description": desc,
              "width": 8,
              "height": 2,
              "data_source": uuid.uuid4()},
             {"name": "Top Of Two",
              "description": desc,
              "width": 4,
              "height": 1,
              "data_source": uuid.uuid4()},
             {"name": "Bottom Of Two",
              "description": desc,
              "height": 1,
              "width": 4,
              "data_source": uuid.uuid4()}],
            [{"name": "Wide Graph",
              "description": desc,
              "width": 12,
              "height": 1,
              "data_source": uuid.uuid4()}]]
