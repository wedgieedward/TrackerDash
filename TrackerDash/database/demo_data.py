import random
import uuid

from copy import deepcopy
from datetime import datetime
from datetime import timedelta

data_source_1 = str(uuid.uuid4())
data_source_2 = str(uuid.uuid4())
data_source_3 = str(uuid.uuid4())
data_source_4 = str(uuid.uuid4())

desc = "Created By TrackerDash for Demo Purposes"
description = "This was created by the -d (demo) flag on startup"


def get_num():
    """
    return a random number between 1 and 10
    """
    return random.randrange(0, 10)


def get_demo_doc(offset):
    """
    get a document that is worthy of demoing
    """
    timestamp = (datetime.utcnow() - timedelta(days=offset))
    return {
        "Alpha": get_num(),
        "Beta": get_num(),
        "Charlie": get_num(),
        "Delta": get_num(),
        "Echo": get_num(),
        "__date": timestamp
    }


def generate_graph_dict_from_name(name):
        """
        creates a correct dictionary to represent a graph dict object
        """
        return deepcopy(
            {"title": name, "dimensions": {"width": 12, "height": 1}})


# Start of demo data constant to be iterated over and
# inserted into the database
DEMO_DATA = (
    # Single Named Data Source
    ('named_data_source', get_demo_doc(5)),
    ('named_data_source', get_demo_doc(4)),
    ('named_data_source', get_demo_doc(3)),
    ('named_data_source', get_demo_doc(2)),
    ('named_data_source', get_demo_doc(1)),

    # Graphs
    ('graph', {
        "title": "Demo Pie Graph",
        "data_source": "named_data_source",
        "description": description,
        "data_range": {
            "days": 7,
            "weeks": 0,
            "hours": 0,
            "minutes": 0,
            "seconds": 0
        },
        "graph_type": "pie",
        "stacked": False,
        "url": 'http://www.google.com'
    }),
    ('graph', {
        "title": "Demo Line Graph",
        "data_source": "named_data_source",
        "description": description,
        "data_range": {
            "days": 7,
            "weeks": 0,
            "hours": 0,
            "minutes": 0,
            "seconds": 0
        },
        "graph_type": "line",
        "stacked": False
    }),
    ('graph', {
        "title": "Demo Line Graph (Stacked)",
        "data_source": "named_data_source",
        "description": description,
        "data_range": {
            "days": 7,
            "weeks": 0,
            "hours": 0,
            "minutes": 0,
            "seconds": 0
        },
        "graph_type": "line",
        "stacked": True
    }),
    ('graph', {
        "title": "Demo Area Graph",
        "data_source": "named_data_source",
        "description": description,
        "data_range": {
            "days": 7,
            "weeks": 0,
            "hours": 0,
            "minutes": 0,
            "seconds": 0
        },
        "graph_type": "area",
        "stacked": False
    }),
    ('graph', {
        "title": "Demo Area Graph (Stacked)",
        "data_source": "named_data_source",
        "description": description,
        "data_range": {
            "days": 7,
            "weeks": 0,
            "hours": 0,
            "minutes": 0,
            "seconds": 0
        },
        "graph_type": "area",
        "stacked": True
    }),
    ('graph', {
        "title": "Demo Column Graph",
        "data_source": "named_data_source",
        "description": description,
        "data_range": {
            "days": 7,
            "weeks": 0,
            "hours": 0,
            "minutes": 0,
            "seconds": 0
        },
        "graph_type": "column",
        "stacked": False
    }),
    ('graph', {
        "title": "Demo Column Graph (Stacked)",
        "data_source": "named_data_source",
        "description": description,
        "data_range": {
            "days": 7,
            "weeks": 0,
            "hours": 0,
            "minutes": 0,
            "seconds": 0
        },
        "graph_type": "column",
        "stacked": True
    }),
    ('graph', {
        "title": "Demo Scatter Graph",
        "data_source": "named_data_source",
        "description": description,
        "data_range": {
            "days": 7,
            "weeks": 0,
            "hours": 0,
            "minutes": 0,
            "seconds": 0
        },
        "graph_type": "scatter",
        "stacked": False
    }),
    ('graph', {
        "title": "Demo Bar Graph",
        "data_source": "named_data_source",
        "description": description,
        "data_range": {
            "days": 7,
            "weeks": 0,
            "hours": 0,
            "minutes": 0,
            "seconds": 0
        },
        "graph_type": "bar",
        "stacked": False
    }),
    ('graph', {
        "title": "Demo Bar Graph (Stacked)",
        "data_source": "named_data_source",
        "description": description,
        "data_range": {
            "days": 7,
            "weeks": 0,
            "hours": 0,
            "minutes": 0,
            "seconds": 0
        },
        "graph_type": "bar",
        "stacked": True
    }),

    # Dashboards
    ('dashboard', {
        "title": "[DEMO] Pie Chart",
        "row_data": [
            [generate_graph_dict_from_name("Demo Pie Graph")]
        ]
    }),
    ('dashboard', {
        "title": "[DEMO] Line Charts",
        "row_data": [
            [generate_graph_dict_from_name("Demo Line Graph")],
            [generate_graph_dict_from_name("Demo Line Graph (Stacked)")]
        ]
    }),
    ('dashboard', {
        "title": "[DEMO] Area Charts",
        "row_data": [
            [generate_graph_dict_from_name("Demo Area Graph")],
            [generate_graph_dict_from_name("Demo Area Graph (Stacked)")]
        ]
    }),
    ('dashboard', {
        "title": "[DEMO] Column Charts",
        "row_data": [
            [generate_graph_dict_from_name("Demo Column Graph")],
            [generate_graph_dict_from_name("Demo Column Graph (Stacked)")]
        ]
    }),
    ('dashboard', {
        "title": "[DEMO] Scatter Chart",
        "row_data": [
            [generate_graph_dict_from_name("Demo Scatter Graph")]
        ]
    }),
    ('dashboard', {
        "title": "[DEMO] Bar Charts",
        "row_data": [
            [generate_graph_dict_from_name("Demo Bar Graph")],
            [generate_graph_dict_from_name("Demo Bar Graph (Stacked)")]
        ]
    }),
    ('showreel', {
        "title": "Demo Showreel",
        "refresh_interval": 15,
        "reels": [
            {
                "title": "[DEMO] Line Charts",
                "item_type": "dashboard"
            },
            {
                "title": "Demo Pie Graph",
                "item_type": 'graph'
            },
            {
                "title": "[DEMO] Area Charts",
                "item_type": "dashboard"
            }
        ]
    })

)
