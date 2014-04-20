import unittest

from TrackerDash import constants
from TrackerDash.common import theme_helpers
from TrackerDash.database.mongo_accessor import TestAccessor


class TestThemeHelpers(unittest.TestCase):
    accessor = TestAccessor()

    def setUp(self):
        for collection in self.accessor.get_local_collections():
            self.accessor.delete_collection(collection)
        self.accessor.add_essential_collections()

    def test_get_defaults(self):
        """
        """
        self.assertEquals(
            theme_helpers.get_default_theme(), constants.DEFAULT_THEME)
        self.assertEquals(
            theme_helpers.get_default_style(), constants.DEFAULT_STYLE)

    def test_get_configured_theme_sets_default(self):
        """
        """
        self.assertIsNone(
            self.accessor.get_one_document_by_query(
                "config", {"config": "theme"}))

        theme_helpers.get_configured_theme(self.accessor)

        theme_document = self.accessor.get_one_document_by_query(
            "config", {"config": "theme"})
        self.assertIsNotNone(theme_document)
        self.assertEquals(
            theme_document["theme"], theme_helpers.get_default_theme())

    def test_get_configured_style_sets_default(self):
        """
        """
        self.assertIsNone(
            self.accessor.get_one_document_by_query(
                "config", {"config": "style"}))

        theme_helpers.get_configured_style(self.accessor)

        style_document = self.accessor.get_one_document_by_query(
            "config", {"config": "style"})
        self.assertIsNotNone(style_document)
        self.assertEquals(
            style_document["style"], theme_helpers.get_default_style())

    def test_set_style(self):
        """
        """
        configured_style = theme_helpers.get_configured_style(self.accessor)
        self.assertIsNotNone(configured_style)

        test_string = "test_style"
        theme_helpers.set_style(self.accessor, test_string)

        new_style = theme_helpers.get_configured_style(self.accessor)
        self.assertNotEquals(new_style, configured_style)
        self.assertEquals(new_style, test_string)

    def test_set_theme(self):
        """
        """
        configured_theme = theme_helpers.get_configured_theme(self.accessor)
        self.assertIsNotNone(configured_theme)

        test_string = "test_theme"
        theme_helpers.set_theme(self.accessor, test_string)

        new_theme = theme_helpers.get_configured_theme(self.accessor)
        self.assertNotEquals(new_theme, configured_theme)
        self.assertEquals(new_theme, test_string)
