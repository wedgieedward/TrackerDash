"""
template for database configuration/information page
"""
from twisted.python.filepath import FilePath
from twisted.web.template import Element, XMLFile, XMLString, renderer

from TrackerDash.database import common as db_common
from TrackerDash.database.mongo_accessor import MongoAccessor


class DatabaseContent(Element):
    """
    DatabaseContent object
    """

    def __init__(self):
        super(DatabaseContent, self).__init__()
        self.loader = XMLFile(
            FilePath("TrackerDash/snippets/configuration.xml"))
        self.accessor = MongoAccessor()

    @renderer
    def header(self, request, tag):
        """
        """
        return 'Database Content Overview'

    @renderer
    def configuration_content(self, request, tag):
        """
        get the list content
        """
        output_string = ""
        output_string += '<div class="list-group">'
        output_string += "<div>"

        output_string += self.get_showreel_xml()
        output_string += self.get_dashboard_xml()
        output_string += self.get_graph_xml()
        output_string += self.get_data_sources_xml()

        output_string += "</div>"
        output_string += "</div>"
        renderable_string = XMLString(output_string)
        return renderable_string.load()

    def get_showreel_xml(self):
        """
        """
        title = "Showreels"
        collection = "showreel"
        string = ""
        number_of_recs = self.accessor.get_number_of_documents_in_collection(
            collection)
        string += self.get_title_string(title, number_of_recs)

        if number_of_recs == 0:
            string += self.get_nothing_configured_list_item()
        else:
            documents = self.accessor.get_all_documents_from_collection(
                collection)
            for document in documents:
                string += self.get_list_item(document["name"])
        return string

    def get_graph_xml(self):
        """
        """
        title = "Graphs"
        collection = "graph"
        string = ""
        number_of_recs = self.accessor.get_number_of_documents_in_collection(
            collection)
        string += self.get_title_string(title, number_of_recs)

        if number_of_recs == 0:
            string += self.get_nothing_configured_list_item()
        else:
            documents = self.accessor.get_all_documents_from_collection(
                collection)
            for document in documents:
                string += self.get_list_item(document["title"])
        return string

    def get_dashboard_xml(self):
        """
        """
        title = "Dashboards"
        collection = "dashboard"
        string = ""
        number_of_recs = self.accessor.get_number_of_documents_in_collection(
            collection)
        string += self.get_title_string(title, number_of_recs)

        if number_of_recs == 0:
            string += self.get_nothing_configured_list_item()
        else:
            documents = self.accessor.get_all_documents_from_collection(
                collection)
            for document in documents:
                name = document["name"]
                badge_number = self.get_number_of_graphs_from_dashboard(
                    document)
                string += self.get_list_item_with_badge(name, badge_number)

        return string

    def get_data_sources_xml(self):
        """
        """
        title = "Data Sources"
        data_sources = db_common.get_configured_data_sources(self.accessor)
        string = ""
        string += self.get_title_string(title, len(data_sources))
        if len(data_sources) == 0:
            string += self.get_nothing_configured_list_item()
        else:
            for data_source in data_sources:
                number_of_recs = (
                    self.accessor.get_number_of_documents_in_collection(
                        data_source))
                string += self.get_list_item_with_badge(
                    data_source, number_of_recs)
        return string

    def get_number_of_graphs_from_dashboard(self, document):
        """
        """
        row_data = document["row_data"]
        counter = 0
        for row in row_data:
            for graph in row:
                counter += 1
        return counter

    def get_title_string(self, title, badge_number):
        """
        get the xml for a title list group object
        """
        return '<a class="list-group-item active"><span class="badge">%d</span>%s</a>' % (
            badge_number,
            title)

    def get_list_item_with_badge(self, text, badge_number):
        """
        get an item for the list group object
        """
        return '<div class="list-group-item"><span class="badge">%d</span>%s</div>' % (
            badge_number, text)

    def get_list_item(self, text):
        """
        get an item for the list group object
        """
        return '<div class="list-group-item">%s</div>' % text

    def get_nothing_configured_list_item(self):
        """
        useful for UI
        """
        return '<div class="list-group-item">Nothing seems to be configured...</div>'
