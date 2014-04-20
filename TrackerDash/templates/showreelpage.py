"""
Graph Page
"""
from twisted.python.filepath import FilePath
from twisted.web.template import renderer, XMLFile

from TrackerDash.templates.basewebpage import BasePage
from TrackerDash.templates.navbar import NavBar
from TrackerDash.templates.showreelpagecontent import ShowreelContent


class ShowreelPage(BasePage):
    display_alarms = False

    def __init__(self, show_reel):
        super(ShowreelPage, self).__init__()
        self.show_reel = show_reel

    @renderer
    def auto_refresh(self, request, tag):
        return ''

    @renderer
    def navbar(self, request, tag):
        """
        return the dashboard
        """
        return NavBar(False)

    @renderer
    def header_scripts(self, request, tag):
        """
        return the header script tags required for this page
        """
        return XMLFile(
            FilePath("TrackerDash/snippets/dashheaderscripts.xml")).load()

    @renderer
    def content(self, request, tag):
        """
        return the content of this page
        """
        return ShowreelContent(self.show_reel)
