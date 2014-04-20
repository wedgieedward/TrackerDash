"""
unit test the schemas
"""
from copy import deepcopy
import unittest
from colander import Invalid
from TrackerDash.schemas import api


class ShowreelItemSchemaSanity(unittest.TestCase):
    def test_valid_showreel_item(self):
        valid_struct = {
            "title": "something",
            "item_type": "graph"
        }
        showreelschema = api.ShowreelItem()
        deserialized = showreelschema.deserialize(valid_struct)
        self.assertEquals(deserialized, valid_struct)

    def test_invalid_itemtype(self):
        invalid_struct = {
            "title": "something",
            "item_type": "invalid"
        }
        showreelschema = api.ShowreelItem()
        self.assertRaises(
            Invalid, showreelschema.deserialize, invalid_struct)


class ShowreelSchemaSanity(unittest.TestCase):
    def test_valid_showreel(self):
        """
        """
        valid_struct = {
            "title": "test_showreel",
            "refresh_interval": 60,
            "reels": [
                {"title": "dashboard name", "item_type": "dashboard"},
                {"title": "graph_name", "item_type": "graph"}
            ]
        }
        showreelschema = api.Showreel()
        deserialized = showreelschema.deserialize(valid_struct)
        self.assertEquals(deserialized, valid_struct)


class DashboardSchemaSanity(unittest.TestCase):
    """
    Test the behavior of the dashboard schema
    """

    def generate_graph_dict_from_name(self, name):
        """
        """
        return deepcopy(
            {"title": name, "dimensions": {"width": 4, "height": 1}})

    def test_one_row(self):
        """
        test what happens with just one graph in a single row
        """
        dashboard_dict = {
            "title": "Edward Post Dashboard Name",
            "row_data": [
                [self.generate_graph_dict_from_name("my_graph")]
            ]
        }
        dashboard_schema = api.Dashboard()
        deserialized = dashboard_schema.deserialize(dashboard_dict)
        self.assertEquals(deserialized, dashboard_dict)

    def test_valid_dashboard(self):
        """
        tests that given a valid dashboard dictionary,
        it deserializes correctly
        """
        dashboard_dict = {
            "title": "Test Dashboard Name",
            "row_data": [
                [
                    self.generate_graph_dict_from_name("graph1"),
                    self.generate_graph_dict_from_name("graph2")
                ],
                [self.generate_graph_dict_from_name("graph3")]]}
        dashboard_schema = api.Dashboard()
        deserialized = dashboard_schema.deserialize(dashboard_dict)
        self.assertEquals(deserialized, dashboard_dict)

        dashboard_dict = {
            "title": "Test Dashboard Name",
            "row_data": [
                [
                    self.generate_graph_dict_from_name("graph1"),
                    self.generate_graph_dict_from_name("graph2")
                ],
                [self.generate_graph_dict_from_name("graph3")]]}

        dashboard_schema = api.Dashboard()
        deserialized = dashboard_schema.deserialize(dashboard_dict)
        self.assertEquals(deserialized, dashboard_dict)

    def test_dashboard_data_with_extra_key(self):
        """
        tests that given a valid dashboard dictionary with extra keys,
        it deserializes correctly
        """
        dashboard_dict = {
            "title": "Test Dashboard Name",
            "row_data": [
                [
                    self.generate_graph_dict_from_name("graph1"),
                    self.generate_graph_dict_from_name("graph2")
                ],
                [self.generate_graph_dict_from_name("graph3")]],
            "extra_key": "value"}

        dashboard_schema = api.Dashboard()
        deserialized = dashboard_schema.deserialize(dashboard_dict)
        self.assertNotEquals(deserialized, dashboard_dict)
        self.assertNotIn("extra_key", deserialized)

    def test_invalid_dashboard_title(self):
        """
        tests invalid dashboard schemas
        """
        # Bad Name
        dashboard_dict = {
            "title": 1234,
            "row_data": [
                [
                    self.generate_graph_dict_from_name("graph1"),
                    self.generate_graph_dict_from_name("graph2")
                ],
                [self.generate_graph_dict_from_name("graph3")]]}

        dashboard_schema = api.Dashboard()
        self.assertRaises(
            Invalid, dashboard_schema.deserialize, dashboard_dict)

    def test_invalid_dashboard_row_data(self):
        """
        tests invalid dashboard schemas
        """
        # Bad Name
        dashboard_dict = {"title": "dashboard title",
                          "row_data": ["graph1", "graph2", "graph3"]}

        dashboard_schema = api.Dashboard()
        self.assertRaises(
            Invalid, dashboard_schema.deserialize, dashboard_dict)


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
                       "data_source": "someuniquestring",
                       "data_range": {"minutes": 0,
                                      "hours": 0,
                                      "days": 0,
                                      "weeks": 1,
                                      "seconds": 0},
                       "graph_type": "area",
                       "stacked": True,
                       "url": "https://www.example.com"
                       }
        graph_schema = api.Graph()
        deserialized = graph_schema.deserialize(valid_graph)
        self.assertEquals(deserialized, valid_graph)

    def test_missing_defaults(self):
        """
        test that a valid graph deserializes
        """
        valid_graph = {"title": "Tall Wide Graph",
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
             "seconds": 0})

    def test_data_range(self):
        """
        tests the behaviour of missing data ranges
        """
        valid_graph = {"title": "Tall Wide Graph",
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


if __name__ == '__main__':
    unittest.main()
