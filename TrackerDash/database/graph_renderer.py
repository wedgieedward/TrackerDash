"""
class for rendering individual graphs
"""
import json
import logging
from TrackerDash.database.mongo_accessor import MongoAccessor

TIME_LINEAR_GRAPH_TYPES = ('line', 'bar', 'area', 'column', 'scatter', 'bar', 'column')
SINGLE_DOCUMENT_GRAPH_TYPES = ("pie")


class HighChartsDataRenderer(object):

    def __init__(self, graph_document):
        self.graph_document = graph_document
        self.data_source = graph_document["data_source"]
        self.accessor = MongoAccessor()
        # This is an array of documents needed for this class to process later.
        self.relevant_data = self.get_relevant_data_for_graph_type()
        self.dictionary = {}
        self.process()

    def render_as_json(self):
        logging.debug(
            "renderering graph: %s as json, output dict: %r" % (
                self.graph_document["title"],
                self.dictionary))
        return json.dumps(self.dictionary)

    def get_relevant_data_for_graph_type(self):
        """
        returns an array of document(s)
        """
        chart_type = self.graph_document["type"]
        if chart_type in TIME_LINEAR_GRAPH_TYPES:
            data_range = self.graph_document["data_range"]
            records = self.accessor.get_all_documents_created_in_last(
                self.data_source,
                weeks=data_range["weeks"],
                days=data_range["days"],
                hours=data_range["hours"],
                minutes=data_range["minutes"])
            return records

        elif chart_type in SINGLE_DOCUMENT_GRAPH_TYPES:
            record = self.accessor.get_last_document_inserted(
                self.data_source)
            return [record]

    def get_plot_options(self):
        """
        """
        options = {'bar': {'dataLabels': {'enabled': True}},
                   'area': {'fillOpacity': 0.5},
                   "pie": {"allowPointSelect": True,
                           "cursor": 'pointer'},
                   "scatter": {"marker": {"radius": 5,
                                          "states": {"hover": {"enabled": True,
                                                               "lineColor": 'rgb(100,100,100)'}
                                                     }
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
        self.dictionary['legend'] = {'layout': 'vertical',
                                     'align': 'right',
                                     'verticalAlign': 'top',
                                     'x': -40,
                                     'y': 100,
                                     'floating': True,
                                     'borderWidth': 1,
                                     'backgroundColor': '#FFFFFF',
                                     'shadow': True
                                     }

    def set_title(self):
        """
        """
        self.dictionary["title"] = {'text': self.graph_document['title']}

    def set_description(self):
        """
        """
        self.dictionary["subtitle"] = {'text': self.graph_document["description"]}

    def set_series_data(self):
        chart_type = self.graph_document["type"]
        series = []
        if chart_type in TIME_LINEAR_GRAPH_TYPES:
            data = {}
            first_doc = self.relevant_data[0]
            keys = first_doc.keys()
            keys.remove("_id")
            for key in keys:
                data[key] = []

            for document in self.relevant_data:
                for key in keys:
                    data[key].append(document[key])

            for key in keys:
                series.append({"name": key, "data": data[key]})

        elif chart_type in SINGLE_DOCUMENT_GRAPH_TYPES:
            document = self.relevant_data[0]
            keys = document.keys()
            keys.remove("_id")
            data = []
            for key in keys:
                data.append([key, document[key]])
            series = [{"type": chart_type,
                       "data": data}]

        self.dictionary["series"] = series

    def set_type(self):
        """
        """
        chart_type = self.graph_document["type"]
        if chart_type in TIME_LINEAR_GRAPH_TYPES:
            self.dictionary["chart"] = {"type": chart_type}

    def process(self):
        """
        process the graph document and relevent data to be able to
        """
        self.set_title()
        self.set_description()
        self.set_plotOptions()
        self.set_series_data()
        self.set_type()
