from bson import objectid
from datetime import datetime
from datetime import timedelta
import uuid
import random

data_source_1 = str(uuid.uuid4())
data_source_2 = str(uuid.uuid4())
data_source_3 = str(uuid.uuid4())
data_source_4 = str(uuid.uuid4())

desc = "Created By TrackerDash for Demo Purposes"


def get_num():
    """
    return a random number between 1 and 10
    """
    return random.randrange(0, 10)


def get_demo_doc(offset):
    """
    get a document that is worthy of demoing
    """
    gen_time = datetime.now() - timedelta(days=offset)
    dummy_id = objectid.ObjectId.from_datetime(gen_time)
    return {
        "_id": dummy_id,
        "Alpha": get_num(),
        "Beta": get_num(),
        "Charlie": get_num(),
        "Delta": get_num(),
        "Echo": get_num()
    }

description = "This was created by the -d (demo) flag on startup"


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
        "width": 12,
        "height": 1,
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
        "stacked": False
    }),
    ('graph', {
        "title": "Demo Line Graph",
        "width": 12,
        "height": 1,
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
        "width": 12,
        "height": 1,
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
        "width": 12,
        "height": 1,
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
        "width": 12,
        "height": 1,
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
        "width": 12,
        "height": 1,
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
        "width": 12,
        "height": 1,
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
        "width": 12,
        "height": 1,
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
        "width": 12,
        "height": 1,
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
        "width": 12,
        "height": 1,
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
        "name": "[DEMO] Pie Chart",
        "row_data": [["Demo Pie Graph"]]
    }),
    ('dashboard', {
        "name": "[DEMO] Line Chart",
        "row_data": [["Demo Line Graph"]]
    }),
    ('dashboard', {
        "name": "[DEMO] Line Chart (Stacked)",
        "row_data": [["Demo Line Graph (Stacked)"]]
    }),
    ('dashboard', {
        "name": "[DEMO] Area Chart",
        "row_data": [["Demo Area Graph"]]
    }),
    ('dashboard', {
        "name": "[DEMO] Area Chart (Stacked)",
        "row_data": [["Demo Area Graph (Stacked)"]]
    }),
    ('dashboard', {
        "name": "[DEMO] Column Chart",
        "row_data": [["Demo Column Graph"]]
    }),
    ('dashboard', {
        "name": "[DEMO] Column Chart (Stacked)",
        "row_data": [["Demo Column Graph (Stacked)"]]
    }),
    ('dashboard', {
        "name": "[DEMO] Scatter Chart",
        "row_data": [["Demo Scatter Graph"]]
    }),
    ('dashboard', {
        "name": "[DEMO] Bar Chart",
        "row_data": [["Demo Bar Graph"]]
    }),
    ('dashboard', {
        "name": "[DEMO] Bar Chart (Stacked)",
        "row_data": [["Demo Bar Graph (Stacked)"]]
    }),

)
