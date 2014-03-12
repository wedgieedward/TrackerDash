import uuid

data_source_1 = uuid.uuid4()
data_source_2 = uuid.uuid4()
data_source_3 = uuid.uuid4()
data_source_4 = uuid.uuid4()

desc = "Created By TrackerDash for DemoPurposes"

DEMO_DATA = (
    ("dashboard",
        {"name": "A Dashboard [DEMO]",
         "row_data": [[{"title": "Tall Wide Graph",
                        "description": desc,
                        "width": 8,
                        "height": 2,
                        "data_source": data_source_1,
                        "data_range": {"minutes": 0,
                                       "hours": 0,
                                       "days": 0,
                                       "weeks": 1,
                                       "months": 0},
                        "type": "area",
                        "stacked": True
                        },

                       {"title": "Tall Thin Graph",
                        "description": desc,
                        "width": 4,
                        "height": 2,
                        "data_source": data_source_2,
                        "data_range": {"minutes": 0,
                                       "hours": 0,
                                       "days": 0,
                                       "weeks": 1,
                                       "months": 0},
                        "type": "pie",
                        "stacked": True

                        }],

                      [{"title": "Wide Graph",
                        "description": desc,
                        "width": 12,
                        "height": 1,
                        "data_source": data_source_4,
                        "data_range": {"minutes": 0,
                                       "hours": 0,
                                       "days": 0,
                                       "weeks": 1,
                                       "months": 0},
                        "type": "line",
                        "stacked": False
                        }]]}),)
