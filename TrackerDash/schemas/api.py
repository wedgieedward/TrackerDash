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


class DataRange(colander.MappingSchema):
    """
    Schema for a data range dictionary
    """
    minutes = colander.SchemaNode(colander.Int(), missing=0)
    hours = colander.SchemaNode(colander.Int(), missing=0)
    days = colander.SchemaNode(colander.Int(), missing=0)
    weeks = colander.SchemaNode(colander.Int(), missing=0)
    seconds = colander.SchemaNode(colander.Int(), missing=0)


class Graph(colander.MappingSchema):
    """
    Schema for a graph document
    """
    title = colander.SchemaNode(colander.String())
    width = colander.SchemaNode(colander.Int(),
                                validator=colander.OneOf([4, 6, 8, 12]))
    height = colander.SchemaNode(colander.Int(),
                                 validator=colander.Range(1, 5))
    data_source = colander.SchemaNode(colander.String())

    # Optional args
    description = colander.SchemaNode(colander.String(), missing="")
    data_range = DataRange(missing={"minutes": 0,
                                    "hours": 0,
                                    "days": 0,
                                    "weeks": 1,
                                    "seconds": 0})
    graph_type = colander.SchemaNode(colander.String(),
                                     validator=colander.OneOf(SUPPORTED_GRAPHS),
                                     missing="line")
    stacked = colander.SchemaNode(colander.Bool(), missing=False)
