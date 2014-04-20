"""
graph container element
"""
import logging

from twisted.web.template import Element, XMLFile, renderer, XMLString
from twisted.python.filepath import FilePath

from TrackerDash.database.mongo_accessor import MongoAccessor


class ShowreelContent(Element):
    """
    Element to handle the content of a dashboard page
    """

    def __init__(self, showreel_name):
        super(ShowreelContent, self).__init__()
        self.loader = XMLFile(
            FilePath("TrackerDash/snippets/graphcontent.xml"))
        self.showreel_name = showreel_name
        self.accessor = MongoAccessor()
        self.showreel_document = self.accessor.get_one_document_by_query(
            "showreel",
            {"title": self.showreel_name})
        logging.debug("Showreel Document: %r" % self.showreel_document)

    @renderer
    def render_content(self, request, tag):
        """
        render the content for the graph container
        """
        if self.showreel_document is not None:
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

        return ""
