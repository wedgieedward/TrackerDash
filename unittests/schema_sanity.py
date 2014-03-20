"""
unit test the schemas
"""
import unittest
from colander import Invalid
from TrackerDash.schemas import api


class DashboardSchemaSanity(unittest.TestCase):
    """
    Test the behavior of the dashboard schema
    """
    def test_one_row(self):
        """
        test what happens with just one graph in a single row
        """
        dashboard_dict = {"name": "Edward Post Dashboard Name", "row_data": [["my_graph"]]}
        dashboard_schema = api.Dashboard()
        deserialized = dashboard_schema.deserialize(dashboard_dict)
        self.assertEquals(deserialized, dashboard_dict)

    def test_valid_dashboard(self):
        """
        tests that given a valid dashboard dictionary, it deserializes correctly
        """
        dashboard_dict = {"name": "Test Dashboard Name",
                          "row_data": [["graph1", "graph2"], ["graph3"]]}

        dashboard_schema = api.Dashboard()
        deserialized = dashboard_schema.deserialize(dashboard_dict)
        self.assertEquals(deserialized, dashboard_dict)

        dashboard_dict = {"name": "Test Dashboard Name",
                          "row_data": [["graph1", "graph2"]]}

        dashboard_schema = api.Dashboard()
        deserialized = dashboard_schema.deserialize(dashboard_dict)
        self.assertEquals(deserialized, dashboard_dict)

    def test_dashboard_data_with_extra_key(self):
        """
        tests that given a valid dashboard dictionary with extra keys, it deserializes correctly
        """
        dashboard_dict = {"name": "Test Dashboard Name",
                          "row_data": [["graph1", "graph2"], ["graph3"]],
                          "extra_key": "value"}

        dashboard_schema = api.Dashboard()
        deserialized = dashboard_schema.deserialize(dashboard_dict)
        self.assertNotEquals(deserialized, dashboard_dict)
        self.assertNotIn("extra_key", deserialized)

    def test_invalid_dashboard_name(self):
        """
        tests invalid dashboard schemas
        """
        # Bad Name
        dashboard_dict = {"name": 1234,
                          "row_data": [["graph1", "graph2"], ["graph3"]]}

        dashboard_schema = api.Dashboard()
        self.assertRaises(Invalid, dashboard_schema.deserialize, dashboard_dict)

    def test_invalid_dashboard_row_data(self):
        """
        tests invalid dashboard schemas
        """
        # Bad Name
        dashboard_dict = {"name": "dashboard name",
                          "row_data": ["graph1", "graph2", "graph3"]}

        dashboard_schema = api.Dashboard()
        self.assertRaises(Invalid, dashboard_schema.deserialize, dashboard_dict)


class GraphSchemaSanity(unittest.TestCase):
    """
    Tests for the graph schema deserialization
    """

    def test_valid_graph_deserializes(self):
        """
        as title
        """
        valid_graph = {"title": "Tall Wide Graph",
                       "description": "Description",
                       "width": 8,
                       "height": 2,
                       "data_source": "someuniquestring",
                       "data_range": {"minutes": 0,
                                      "hours": 0,
                                      "days": 0,
                                      "weeks": 1,
                                      "months": 0},
                       "graph_type": "area",
                       "stacked": True
                       }
        graph_schema = api.Graph()
        deserialized = graph_schema.deserialize(valid_graph)
        self.assertEquals(deserialized, valid_graph)

    def test_missing_defaults(self):
        """
        test that a valid graph deserializes
        """
        valid_graph = {"title": "Tall Wide Graph",
                       "width": 8,
                       "height": 2,
                       "data_source": "someuniquestring"}
        graph_schema = api.Graph()
        deserialized = graph_schema.deserialize(valid_graph)
        self.assertNotEquals(deserialized, valid_graph)

        # Stacked should be added and defaulted
        self.assertIn("stacked", deserialized)
        self.assertEquals(deserialized["stacked"], False)

        # graph_type should be added and defaulted
        self.assertIn("graph_type", deserialized)
        self.assertEquals(deserialized["graph_type"], 'line')

        # description should be added and defaulted
        self.assertIn("description", deserialized)
        self.assertEquals(deserialized["description"], '')

        # data_range should be added and defaulted
        self.assertIn("data_range", deserialized)
        self.assertEquals(
            deserialized["data_range"],
            {"minutes": 0,
             "hours": 0,
             "days": 0,
             "weeks": 1,
             "months": 0})

    def test_data_range(self):
        """
        tests the behaviour of missing data ranges
        """
        valid_graph = {"title": "Tall Wide Graph",
                       "width": 8,
                       "height": 2,
                       "data_source": "someuniquestring",
                       "data_range": {}}
        graph_schema = api.Graph()
        deserialized = graph_schema.deserialize(valid_graph)
        self.assertNotEquals(deserialized, valid_graph)
        for key in deserialized["data_range"]:
            self.assertEquals(deserialized["data_range"][key], 0)

        valid_graph["data_range"] = {"days": 7}
        deserialized = graph_schema.deserialize(valid_graph)
        self.assertNotEquals(deserialized, valid_graph)

        self.assertEquals(deserialized["data_range"]["days"], 7)

    def test_width_validation(self):
        """
        tests that having a graph of width other than 4, 6, 8 or 12 is rejected
        """
        valid_graph = {"title": "Tall Wide Graph",
                       "width": 8,
                       "height": 1,
                       "data_source": "someuniquestring",
                       "data_range": {}}
        graph_schema = api.Graph()
        deserialized = graph_schema.deserialize(valid_graph)
        self.assertNotEquals(deserialized, valid_graph)

        valid_widths = (4, 6, 8, 12)

        for x in range(13):  # 0, 1, 2, .. , 12
            valid_graph["width"] = x
            if x in valid_widths:
                # This should pass without any errors
                deserialized = graph_schema.deserialize(valid_graph)
                self.assertNotEquals(deserialized, valid_graph)
            else:
                self.assertRaises(Invalid, graph_schema.deserialize, valid_graph)

        # lets test it against things other than ints for kicks
        valid_graph["width"] = "string"
        self.assertRaises(Invalid, graph_schema.deserialize, valid_graph)
        valid_graph["width"] = {"key": "value"}
        self.assertRaises(Invalid, graph_schema.deserialize, valid_graph)

    def test_height_validation(self):
        """
        test that having a graph height of >5
        """
        valid_graph = {"title": "Tall Wide Graph",
                       "width": 8,
                       "height": 1,
                       "data_source": "someuniquestring",
                       "data_range": {}}
        graph_schema = api.Graph()
        deserialized = graph_schema.deserialize(valid_graph)
        self.assertNotEquals(deserialized, valid_graph)

        valid_heights = range(1, 6)  # 1-5

        for x in range(10):  # 0, 1, 2, .. , 9
            valid_graph["height"] = x
            if x in valid_heights:
                # This should pass without any errors
                deserialized = graph_schema.deserialize(valid_graph)
                self.assertNotEquals(deserialized, valid_graph)
            else:
                self.assertRaises(Invalid, graph_schema.deserialize, valid_graph)

        # lets test it against things other than ints for kicks
        valid_graph["height"] = "string"
        self.assertRaises(Invalid, graph_schema.deserialize, valid_graph)
        valid_graph["height"] = {"key": "value"}
        self.assertRaises(Invalid, graph_schema.deserialize, valid_graph)


if __name__ == '__main__':
    unittest.main()
