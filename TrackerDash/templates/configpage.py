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
        config_content = XMLFile(FilePath("TrackerDash/snippets/configuration.xml"))
        return config_content.load()

    @renderer
    def auto_refresh(self, request, tag):
        """
        render the auto refresh meta tag
        """
        return ""

    @renderer
    def alarms(self, request, tag):
        """
        """
        return ""
