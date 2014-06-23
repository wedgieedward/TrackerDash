import json
import logging

from TrackerDash.database.graph_data_renderer import DataRenderer
from TrackerDash.database.mongo_accessor import MongoAccessor


class BaseGraphConstructor(object):
    """
    Base Graph Constructor Object
    """
    charting_library = None

    def __init__(self, graph_document):
        self._graph_document = graph_document
        self.accessor = MongoAccessor()
        self.data_renderer = DataRenderer(self._graph_document)
        self.relevent_data = self.data_renderer.relevent_data
        self.graph_dictionary = {}
        self.graph_type = self._graph_document.get(
            "graph_type",
            "line")

    def process(self):
        """
        apply all the configuration to the graph_dictionary
        so that render methods can be called on it
        """
        self.set_title()
        self.set_description()
        self.set_graph_hyperlink()
        self.set_graph_type()
        self.set_plot_options()
        self.set_series_data()
        self.apply_theme_settings()

    def render_as_json(self):
        """
        render the graph
        """
        logging.debug(
            "redering graph %s as %s. Data %s" % (
                self._graph_document["title"],
                self.charting_library,
                self.graph_dictionary
            )
        )
        return json.dumps(self.graph_dictionary)

    def set_title(self):
        """
        Set the title of the graph
        """
        raise NotImplementedError("Tried calling on base class")

    def set_description(self):
        """
        set the graph description
        """
        raise NotImplementedError("Tried calling on base class")

    def set_graph_hyperlink(self):
        """
        set the graph hyperlink
        """
        raise NotImplementedError("Tried calling on base class")

    def set_graph_type(self):
        """
        set the graph type
        """
        raise NotImplementedError("Tried calling on base class")

    def set_series_data(self):
        """
        apply the output of the data renderer to the graph
        """
        raise NotImplementedError("Tried calling on base class")

    def apply_theme_settings(self):
        """
        apply the configured display theme for this graph
        """
        raise NotImplementedError("Tried calling on base class")

    def set_plot_options(self):
        """
        apply the plot options for the graph
        """
        raise NotImplementedError("Tried calling on base class")
