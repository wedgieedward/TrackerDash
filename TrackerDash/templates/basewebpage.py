"""
base web page
"""
from twisted.web.template import Element, XMLFile, renderer
from twisted.python.filepath import FilePath

from navbar import NavBar


class BasePage(Element):
    """
    Object for base webpage
    """
    display_alarms = False

    def __init__(self):
        super(BasePage, self).__init__()
        self.loader = XMLFile(FilePath("TrackerDash/pages/basewebpage.html"))

    @renderer
    def metadata(self, request, tag):
        """
        render the metadata for the page
        """
        return XMLFile(FilePath('TrackerDash/snippets/metadata.xml')).load()

    @renderer
    def auto_refresh(self, request, tag):
        """
        render the auto refresh meta tag
        """
        return ''

    @renderer
    def required_stylesheets(self, request, tag):
        """
        return the xml required for the stylesheets for this page
        """
        return XMLFile(FilePath("TrackerDash/snippets/stylesheets.xml")).load()

    @renderer
    def favicons(self, request, tag):
        """
        return the xml required for the favicon and touch icons
        """
        return XMLFile(FilePath("TrackerDash/snippets/favicons.xml")).load()

    @renderer
    def header_scripts(self, request, tag):
        """
        return the header script tags required for this page
        """
        return XMLFile(FilePath("TrackerDash/snippets/headerscripts.xml")).load()

    @renderer
    def navbar(self, request, tag):
        """
        return the dashboard
        """
        return NavBar(None)

    @renderer
    def footer(self, request, tag):
        """
        dynamically render the footer
        """
        footer_snippet = XMLFile(FilePath("TrackerDash/snippets/footer.xml"))
        return footer_snippet.load()

    @renderer
    def alarms(self, request, tag):
        """
        dynamically render the alarms
        """
        if not self.display_alarms:
            return ''
        else:
            alarm_snippet = XMLFile(FilePath("TrackerDash/snippets/green_alarm.xml"))
            return alarm_snippet.load()

    @renderer
    def content(self, request, tag):
        """
        This should be overriden on a per page-type basis.
        We will just return nothing here
        """
        return XMLFile(FilePath("TrackerDash/snippets/welcomecontainer.xml")).load()
