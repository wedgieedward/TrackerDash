"""
Template for a display page for a graph
Very similar to a dashpage without the header or footer
"""
from twisted.python.filepath import FilePath
from twisted.web.template import renderer, XMLString, XMLFile

from TrackerDash.templates.basewebpage import BasePage
from TrackerDash.templates.dashcontent import DashContent
from TrackerDash.templates.graphcontent import GraphContent
from TrackerDash.templates.showreelpagecontent import ShowreelContent
from TrackerDash.templates.theme_loader import ThemeLoader


class DisplayPage(BasePage):
    """
    DisplayPage object
    """
    refresh_interval = 60

    def __init__(self, item_to_display, item_type):
        self.item_to_display = item_to_display
        self.item_type = item_type
        super(DisplayPage, self).__init__()

    @renderer
    def auto_refresh(self, request, tag):
        if self.item_type == 'showreel':
            return ''
        return XMLString(
            '<meta http-equiv="refresh" content="%s"></meta>' % (
                self.refresh_interval)).load()

    @renderer
    def header_scripts(self, request, tag):
        """
        return the header script tags required for this page
        """
        return XMLFile(
            FilePath("TrackerDash/snippets/displayheaderscripts.xml")).load()

    @renderer
    def required_stylesheets(self, request, tag):
        """
        return the xml required for the stylesheets for this page
        """
        return ThemeLoader(2)

    @renderer
    def content(self, request, tag):
        """
        return the content of this page
        """
        if self.item_type == 'dashboard':
            return DashContent(self.item_to_display)
        elif self.item_type == 'graph':
            return GraphContent(self.item_to_display)
        elif self.item_type == 'showreel':
            return ShowreelContent(self.item_to_display)

    @renderer
    def navbar(self, request, tag):
        """
        we do not want to display the navbar
        """
        return ""

    # @renderer
    # def footer(self, request, tag):
    #     """
    #     we do not want to render the footer
    #     """
    #     return ""
