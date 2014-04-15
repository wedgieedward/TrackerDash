"""
configuration page
"""
from twisted.web.template import renderer
from TrackerDash.templates.appearance_configuration import AppearanceContent
from TrackerDash.templates.basewebpage import BasePage
from TrackerDash.templates.database_configuration import DatabaseContent


class ConfigPage(BasePage):
    """
    configuration page
    """

    def __init__(self, page_name):
        super(ConfigPage, self).__init__()
        self.page_name = page_name

    @renderer
    def content(self, request, tag):
        """
        get the content for the configuration page
        """
        if self.page_name == 'database':
            return DatabaseContent()
        elif self.page_name == 'appearance':
            return AppearanceContent()

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
