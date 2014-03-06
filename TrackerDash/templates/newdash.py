"""
New Dashboard Page Template
"""

from twisted.web.template import XMLFile, renderer
from twisted.python.filepath import FilePath
from basewebpage import BasePage


class NewDash(BasePage):
    """
    configuration page
    """

    def __init__(self):
        super(NewDash, self).__init__()

    @renderer
    def content(self, request, tag):
        """
        get the content for the configuration page
        """
        footer_snippet = XMLFile(FilePath("TrackerDash/snippets/new_dash.xml"))
        return footer_snippet.load()

    @renderer
    def auto_refresh(self, request, tag):
        """
        render the auto refresh meta tag
        """
        return ""
