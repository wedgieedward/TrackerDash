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


if __name__ == '__main__':
    unittest.main()
