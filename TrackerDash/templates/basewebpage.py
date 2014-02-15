"""
base web page
"""
import logging
from twisted.web.template import Element, XMLFile, renderer, tags
from twisted.python.filepath import FilePath


class BasePage(Element):
    """
    Object for base webpage
    """
    def __init__(self):
        super(BasePage, self).__init__()
        self.loader = XMLFile(FilePath("TrackerDash/pages/basewebpage.html"))

    @renderer
    def head(self, request, tag):
        """
        The head of the base page
        """


    # @renderer
    # def header(self, request, tag):
    #     return tag(tags.b('Header.'))

    # @renderer
    # def content(self, request, tag):
    #     return tag(tags.i('Content. Available Element Methods: %s' % dir(Element)))

    # @renderer
    # def footer(self, request, tag):
    #     return tag(tags.b('Footer.'))
