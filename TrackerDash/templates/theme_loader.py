"""
module to handle theme handling
"""
import logging

from twisted.python.filepath import FilePath
from twisted.web.template import Element, XMLFile, XMLString, renderer

from TrackerDash.common import theme_helpers
from TrackerDash.database.mongo_accessor import MongoAccessor


class ThemeLoader(Element):

    themes = theme_helpers.get_configured_themes()

    def __init__(self):
        super(ThemeLoader, self).__init__()
        self.loader = XMLFile(FilePath("TrackerDash/snippets/stylesheets.xml"))
        self.accessor = MongoAccessor()

    @renderer
    def theme_link(self, request, tag):
        link_string = (
            '<link href="../web/css/custom/%s/bootstrap.min.css" rel="stylesheet"> </link>' % (
                theme_helpers.get_configured_theme(self.accessor)
            )
        )
        string = XMLString(link_string)
        return string.load()

