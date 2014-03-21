"""
helper api utilities
"""
import collections
from colander import Invalid

from TrackerDash.schemas.api import Dashboard
from TrackerDash.schemas.api import Graph


class TransformedDict(collections.MutableMapping):
    """A dictionary that applies an arbitrary key-altering
       function before accessing the keys"""

    def __init__(self, *args, **kwargs):
        self.store = dict()
        self.update(dict(*args, **kwargs))  # use the free update to set keys

    def __getitem__(self, key):
        return self.store[self.__keytransform__(key)]

    def __setitem__(self, key, value):
        self.store[self.__keytransform__(key)] = value

    def __delitem__(self, key):
        del self.store[self.__keytransform__(key)]

    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        return len(self.store)

    def __keytransform__(self, key):
        return key


class BaseSchemaObject(TransformedDict):
    """
    Object for a base schema object
    """

    schema = None

    def validate(self):
        """
        check that we are valid
        """
        try:
            self.schema.deserialize(self.store)
            return (True, "Safe To Upload")
        except Invalid as invalid:
            return (False, invalid.asdict())


class DashboardObject(BaseSchemaObject):
    """
    Implements a shell of a Dashboard Object
    Required Keys:
        name: (string)
        row_data: [[graph1_in_row1, graph2_in_row2], [graph1_in_row_2]]
    """
    schema = Dashboard()


class GraphObject(BaseSchemaObject):
    """
    Implements a shell of a Graph Object
    Required Keys:
        title: (string)
        width: (int: [4, 6, 8, 12])
        height: (int: 1-5)
        data_source: (string)

    Optional Keys:
        description: (string, default: '')
        data_range: (dict: see below, default {'weeks': 1})
        graph_type: (string: default: 'line')
        stacked: (boolean: default: False)
    """
    schema = Graph()
