import unittest

from TrackerDash.templates.navbar import NavBar
from TrackerDash.database.mongo_accessor import TestAccessor


class NavBarSanity(unittest.TestCase):
    """
    """
    def setUp(self):
        self.nav_bar = NavBar(None)
        self.test_accessor = TestAccessor()
        self.nav_bar.accessor = self.test_accessor
        self.test_accessor.reset_all()

    def test_get_dash_names(self):
        """
        tests that the object inheretance works as expected
        """
        dashboards = self.nav_bar.get_dashboards()
        self.assertEquals(len(dashboards), 0)
        test_dash_name = "test-dash-name"
        self.test_accessor.add_document_to_collection("dashboard", {"name": test_dash_name})

        dashboards = self.nav_bar.get_dashboards()
        self.assertEquals(len(dashboards), 1)
        self.assertIn(test_dash_name, dashboards)


if __name__ == '__main__':
    unittest.main()
