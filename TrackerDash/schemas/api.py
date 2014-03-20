"""
Schemas needed to validate incoming api requests
"""

import colander

SUPPORTED_GRAPHS = ('line', 'bar', 'area', 'column', 'scatter', 'bar', 'column', "pie")


class GraphRow(colander.SequenceSchema):
    """
    a list of graph names
    """
    graph_name = colander.SchemaNode(colander.String())


class GraphRows(colander.SequenceSchema):
    """
    A list of graph rows
    """
    row = GraphRow()


class Dashboard(colander.MappingSchema):
    """
    Schema for a dashboard document
    """
    name = colander.SchemaNode(colander.String())
    row_data = GraphRows()


class Graph(colander.MappingSchema):
    """
    Schema for a graph document
    """
    title = colander.SchemaNode(colander.String())
    description = colander.SchemaNode(colander.String())
    data_source = colander.SchemaNode(colander.String())
    stacked = colander.SchemaNode(colander.Bool())
    graph_type = colander.OneOf(SUPPORTED_GRAPHS)
    width = colander.SchemaNode(colander.Int(),
                                validator=colander.OneOf(4, 6, 8, 12))
    height = colander.SchemaNode(colander.Int(),
                                 validator=colander.Range(1, 5))
