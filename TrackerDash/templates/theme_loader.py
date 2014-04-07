"""
module to handle theme handling
"""
import logging

from twisted.python.filepath import FilePath
from twisted.web.template import Element, XMLFile, XMLString, renderer

from TrackerDash.database.mongo_accessor import MongoAccessor


class ThemeLoader(Element):

    default_theme = 'cosmo'
    themes = (
        'amelia',
        'bootstrap',
        'cerulean',
        'cosmo',
        'cyborg',
        'darkly',
        'flatly',
        'journal',
        'lumen',
        'readable',
        'simplex',
        'slate',
        'spacelab',
        'united',
        'yeti',
    )

    def __init__(self):
        super(ThemeLoader, self).__init__()
        self.loader = XMLFile(FilePath("TrackerDash/snippets/stylesheets.xml"))
        self.accessor = MongoAccessor()

    @renderer
    def theme_link(self, request, tag):
        link_string = (
            '<link href="../web/css/custom/%s/bootstrap.min.css" rel="stylesheet"> </link>' % (
                self.get_configured_theme()
            )
        )
        string = XMLString(link_string)
        return string.load()

    def get_configured_theme(self):
        """
        go to the configuration and get the saved theme
        """
        theme_document = self.accessor.get_one_document_by_query('config', {'config': 'theme'})
        if theme_document is None:
            logging.info("No theme found, adding default theme")
            theme = self.get_default_theme()
            self.set_theme(theme)
        else:
            theme = theme_document["theme"]
        return theme

    def get_default_theme(self):
        """
        get the default theme
        """
        return self.default_theme

    def set_theme(self, theme):
        """
        set a theme
        """
        logging.info("Setting application theme: %s" % theme)
        self.accessor.remove_documents_by_query('config', {"config": "theme"})
        self.accessor.add_document_to_collection('config', {"config": 'theme', "theme": theme})
