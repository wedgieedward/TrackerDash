"""
configuration page
"""
from twisted.web.template import renderer
from TrackerDash.templates.basewebpage import BasePage
from TrackerDash.templates.database_configuration import DatabaseContent


class ConfigPage(BasePage):
    """
    configuration page
    """

    def __init__(self):
        super(ConfigPage, self).__init__()

    @renderer
    def content(self, request, tag):
        """
        get the content for the configuration page
        """
        return DatabaseContent()

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
