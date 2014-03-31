"""
class for rendering individual graphs
"""
from bson import objectid
import json
import logging
import time
from TrackerDash.database.mongo_accessor import MongoAccessor

TIME_LINEAR_GRAPH_TYPES = ('line', 'bar', 'area', 'column', 'scatter', 'bar', 'column')
SINGLE_DOCUMENT_GRAPH_TYPES = ("pie")


class HighChartsDataRenderer(object):
    # If there is a lot of data, use every nth document instead
    OPTIMISE_AMOUNT = 5
    # Number of records where we should start optimising
    OPTIMISE_BOUNDRY = 1000

    def __init__(self, graph_document):
        self.graph_document = graph_document
        self.data_range = self.graph_document["data_range"]
        self.data_source = graph_document["data_source"]
        self.accessor = MongoAccessor()
        # This is an array of documents needed for this class to process later.
        self.relevent_data = self.get_relevent_data_for_graph_type()
        self.optimise_relevent_data()
        self.dictionary = {}
        self.process()

    def process(self):
        """
        process the graph document and relevent data to be able to
        """
        self.set_title()
        self.set_description()
        self.set_plotOptions()
        self.set_series_data()
        self.set_type()

    def render_as_json(self):
        logging.debug(
            "renderering graph: %s as json, output dict: %r" % (
                self.graph_document["title"],
                self.dictionary))
        return json.dumps(self.dictionary)

    def get_relevent_data_for_graph_type(self):
        """
        returns an array of document(s)
        """
        chart_type = self.graph_document["graph_type"]
        if chart_type in TIME_LINEAR_GRAPH_TYPES:
            records = self.accessor.get_all_documents_created_in_last(
                self.data_source,
                **self.data_range)
            return records

        elif chart_type in SINGLE_DOCUMENT_GRAPH_TYPES:
            record = self.accessor.get_last_document_inserted(
                self.data_source)
            return [record]

    def get_plot_options(self):
        """
        """
        options = {
            'bar': {
                'dataLabels': {
                    'enabled': True
                }
            },
            'area': {
                'fillOpacity': 0.5,
                'marker': {
                    "enabled": False
                }
            },
            "pie": {
                "allowPointSelect": True,
                "cursor": 'pointer',
                "dataLabels": {
                    "enabled": True,
                    "inside": True
                },
                # "showInLegend": True
            },
            "scatter": {
                "marker": {
                    "radius": 5,
                    "states": {
                        "hover": {
                            "enabled": True,
                            "lineColor": 'rgb(100,100,100)'
                        }
                    }
                }
            },
            "line": {
                "marker": {
                    "enabled": False
                }
            },
        }

        if self.graph_document["stacked"]:
            options["series"] = {"stacking": "normal"}

        return options

    def set_plotOptions(self):
        """
        """
        self.dictionary["plotOptions"] = self.get_plot_options()
        self.dictionary["credits"] = {"enabled": False}
        # self.dictionary['legend'] = {'layout': 'vertical',
        #                              'align': 'right',
        #                              'verticalAlign': 'top',
        #                              'x': -40,
        #                              'y': 100,
        #                              'floating': True,
        #                              'borderWidth': 1,
        #                              'backgroundColor': '#FFFFFF',
        #                              'shadow': True
        #                              }

    def set_title(self):
        """
        """
        self.dictionary["title"] = {'text': self.graph_document['title']}

    def set_description(self):
        """
        """
        self.dictionary["subtitle"] = {'text': self.graph_document["description"]}

    def set_series_data(self):
        chart_type = self.graph_document["graph_type"]
        series = []
        if chart_type in TIME_LINEAR_GRAPH_TYPES:
            data = {}
            if len(self.relevent_data) != 0:
                first_doc = self.relevent_data[0]
                keys = first_doc.keys()
                keys.remove("_id")

                # Sort the keys and make them pretty to display (title)
                keys.sort()
                for key in keys:
                    data[key] = []

                for document in self.relevent_data:
                    # Get the generation time
                    bson_id = objectid.ObjectId(document["_id"])
                    datetime = bson_id.generation_time

                    # Convert to utc time in miliseconds
                    for_web = time.mktime(datetime.timetuple()) * 1000

                    for key in keys:
                        data[key].append([for_web, document[key]])

                for key in keys:
                    series.append({"name": key, "data": data[key]})

        elif chart_type in SINGLE_DOCUMENT_GRAPH_TYPES:
            document = self.relevent_data[0]
            keys = document.keys()
            keys.remove("_id")
            keys.sort()
            data = []
            for key in keys:
                data.append([key, document[key]])
            series = [{"type": chart_type,
                       "data": data}]

        self.dictionary["series"] = series

    def set_type(self):
        """
        """
        chart_type = self.graph_document["graph_type"]
        if chart_type in TIME_LINEAR_GRAPH_TYPES:
            self.dictionary["chart"] = {"type": chart_type}
            self.dictionary["xAxis"] = {
                "type": 'datetime',
                "title": {
                    "text": self.get_timeseries_axis_title(),
                    "align": "high"
                }
            }
            self.dictionary["yAxis"] = {"title": ''}

    def get_timeseries_axis_title(self):
        """
        generate a title based on self.data_range
        """
        order = [
            "weeks",
            "days",
            "hours",
            "minutes"
        ]
        appended_string = ""
        for key in order:
            if self.data_range[key] != 0:
                appended_string += "%s %s " % (self.data_range[key], key)

        title = "data for the last: %s" % appended_string
        return title.title()

    def optimise_relevent_data(self):
        """

        """
        if len(self.relevent_data) > self.OPTIMISE_BOUNDRY:
            logging.debug("Optimising graph data")
            self.relevent_data = self.relevent_data[0::self.OPTIMISE_AMOUNT]
