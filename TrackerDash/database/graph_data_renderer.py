"""
class for rendering individual graphs
"""
import logging
from TrackerDash.constants import TIME_LINEAR_GRAPH_TYPES
from TrackerDash.constants import SINGLE_DOCUMENT_GRAPH_TYPES
from TrackerDash.database.mongo_accessor import MongoAccessor


class DataRenderer(object):
    def __init__(self, graph_document, optimise_factor=5, optimise_limit=1000):
        # reduce the data size by 1/optimise_factor
        self.optimise_factor = optimise_factor
        # the point at which data should be optimised
        self.optimise_limit = optimise_limit

        self.graph_document = graph_document
        self.data_range = self.graph_document["data_range"]
        self.data_source = graph_document["data_source"]
        self.accessor = MongoAccessor()

        # This is an array of documents needed for this class to process later.
        self.relevent_data = self.get_relevent_data_for_graph_type()
        self.optimise_relevent_data()

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

    def optimise_relevent_data(self):
        """
        Will reduce the number of data points to render for speed-up
        """
        if len(self.relevent_data) > self.optimise_limit:
            logging.debug("Optimising graph data")
            self.relevent_data = self.relevent_data[0::self.optimise_factor]
