"""
configuration page
"""
from twisted.web.template import XMLFile, renderer
from twisted.python.filepath import FilePath
from basewebpage import BasePage


class ConfigPage(BasePage):
    """
    configuration page
    """
    auto_refresh = False

    def __init__(self):
        super(ConfigPage, self).__init__()

    @renderer
    def content(self, request, tag):
        """
        get the content for the configuration page
        """
        footer_snippet = XMLFile(FilePath("TrackerDash/snippets/configuration.xml"))
        return footer_snippet.load()

    @renderer
    def auto_refresh(self, request, tag):
        """
        render the auto refresh meta tag
        """
        return ""
