"""
Object to construct a graph
"""
from copy import deepcopy
import json
import logging
import time

from TrackerDash.common import theme_helpers
from TrackerDash.constants import TIME_LINEAR_GRAPH_TYPES
from TrackerDash.constants import SINGLE_DOCUMENT_GRAPH_TYPES
from TrackerDash.database.graph_data_renderer import DataRenderer
from TrackerDash.database.mongo_accessor import MongoAccessor
from TrackerDash.graphing import styles


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


class HighchartsConstructor(BaseGraphConstructor):
    """
    constructs a configured highcharts object
    """
    charting_library = 'highcharts'

    def set_title(self):
        """
        Set the title of the graph
        """
        self.graph_dictionary.update(
            {
                "title": {
                    "text": self._graph_document.get(
                        "title",
                        "Untitled Graph")
                }
            }
        )

    def set_description(self):
        """
        set the graph description
        """
        self.graph_dictionary.update(
            {
                "subtitle": {
                    "text": self._graph_document.get(
                        "description",
                        "")
                }
            }
        )

    def set_graph_hyperlink(self):
        """
        set the graph hyperlink
        """
        href = self._graph_document.get("url", '')
        self.graph_dictionary.update(
            {
                "credits": {
                    "enabled": bool(href),  # '' = False
                    "href": href,
                    "text": href,
                }
            }
        )

    def set_graph_type(self):
        """
        set the graph type
        """
        if self.graph_type in TIME_LINEAR_GRAPH_TYPES:
            self.graph_dictionary.update(
                {
                    "chart": {
                        "type": self.graph_type
                    },
                    "xAxis": {
                        "type": "datetime",
                        "title": {
                            "text": self.get_timeseries_axis_title(),
                        }
                    },
                }
            )
        stacked = self._graph_document.get("stacked", '')
        if bool(stacked):
            self.graph_dictionary.update(
                {
                    'plotOptions': {
                        "series": {
                            "stacking": "normal"
                        }
                    }
                }
            )

    def set_series_data(self):
        """
        apply the output of the data renderer to the graph
        """
        series = []
        if self.graph_type in TIME_LINEAR_GRAPH_TYPES:
            data = {}
            if len(self.relevent_data) != 0:
                first_doc = self.relevent_data[0]
                keys = first_doc.keys()
                keys.remove("_id")
                keys.remove("__date")

                # Sort the keys and make them pretty to display (title)
                keys.sort()
                for key in keys:
                    data[key] = []

                for document in self.relevent_data:
                    # Get the generation time
                    datetime = document["__date"]
                    del document["__date"]

                    # Convert to utc time in miliseconds
                    for_web = time.mktime(datetime.timetuple()) * 1000

                    for key in keys:
                        data[key].append([for_web, document.get(key, 0)])

                for key in keys:
                    series.append({"name": key, "data": data[key]})

        elif self.graph_type in SINGLE_DOCUMENT_GRAPH_TYPES:
            document = self.relevent_data[0]
            keys = document.keys()
            keys.remove("_id")
            keys.remove("__date")
            keys.sort()
            data = []
            for key in keys:
                data.append([key, document.get(key, 0)])
            series = [{"type": self.graph_type,
                       "data": data}]

        self.graph_dictionary["series"] = series

    def apply_theme_settings(self):
        """
        apply the configured display theme for this graph
        """
        style = theme_helpers.get_configured_style(self.accessor)
        style_dict = styles.get_style_dict(style)
        if style_dict is not None:
            self.graph_dictionary = styles.mergedicts(
                deepcopy(self.graph_dictionary),
                deepcopy(style_dict))

    def get_timeseries_axis_title(self):
        """
        generate a title based on self._graph_document["data_range"]
        """
        order = [
            "weeks",
            "days",
            "hours",
            "minutes"
        ]
        appended_string = ""
        for key in order:
            if self._graph_document["data_range"][key] != 0:
                appended_string += "%s %s " % (
                    self._graph_document["data_range"][key], key)

        title = "data for the last: %s" % appended_string
        return title.title()
