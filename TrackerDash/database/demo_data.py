import uuid

data_source_1 = uuid.uuid4()
data_source_2 = uuid.uuid4()
data_source_3 = uuid.uuid4()
data_source_4 = uuid.uuid4()

desc = "Created By TrackerDash for DemoPurposes"

DEMO_DATA = (
    ("dashboard",
        {"name": "A Dashboard [DEMO]",
         "row_data": [[{"name": "Big Graph",
                       "description": desc,
                       "width": 8,
                       "height": 2,
                       "data_source": data_source_1},
                      {"name": "Top Of Two",
                       "description": desc,
                       "width": 4,
                       "height": 1,
                       "data_source": data_source_2},
                      {"name": "Bottom Of Two",
                       "description": desc,
                       "height": 1,
                       "width": 4,
                       "data_source": data_source_3}],
                     [{"name": "Wide Graph",
                       "description": desc,
                       "width": 12,
                       "height": 1,
                       "data_source": data_source_4}]]}),)
