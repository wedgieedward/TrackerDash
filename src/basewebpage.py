"""
base web page
"""
from twisted.web.template import Element, XMLFile, renderer, tags
from twisted.python.filepath import FilePath


class BaseWebPage(Element):
    """
    Object for base webpage
    """
    def __init__(self, path):
        super(BaseWebPage, self).__init__()
        self.loader = XMLFile(FilePath(path))

    @renderer
    def header(self, request, tag):
        return tag(tags.b('Header.'))

    @renderer
    def footer(self, request, tag):
        return tag(tags.b('Footer.'))
