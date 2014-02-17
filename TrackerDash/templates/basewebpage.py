"""
base web page
"""
from twisted.web.template import Element, XMLFile, renderer
from twisted.python.filepath import FilePath


class BasePage(Element):
    """
    Object for base webpage
    """
    def __init__(self, dashboard=''):
        super(BasePage, self).__init__()
        self.dashboard = dashboard
        self.loader = XMLFile(FilePath("TrackerDash/pages/basewebpage.html"))

    def get_dashboards(self):
        """
        get all configured dashboards
        """
        return [("Dalby Dashboard", 'http://localhost:8090/dash/Dalby Dashboard'),
                ("VCS Dashboard", 'http://localhost:8090/dash/VCS Dashboard'),
                ("Some Other Dashboard", 'http://localhost:8090/dash/Some Other Dashboard')]

    @renderer
    def footer(self, request, tag):
        """
        dynamically render the footer
        """
        footer_snippet = XMLFile(FilePath("TrackerDash/snippets/footer.xml"))
        return footer_snippet.load()

    @renderer
    def dashboards_dropdown(self, request, tag):
        for dashboard, link in self.get_dashboards():
            yield tag.clone().fillSlots(dashName=dashboard, dashLink=link)

    @renderer
    def alarms(self, request, tag):
        """
        dynamically render the alarms
        """
        if self.dashboard != '':
            print "Dashboard: '%s'" % self.dashboard
            return ''
        else:
            alarm_snippet = XMLFile(FilePath("TrackerDash/snippets/green_alarm.xml"))
            return alarm_snippet.load()

    @renderer
    def content(self, request, tag):
        """
        This should be overriden on a per page-type basis.
        We will just return text here
        """
        content_snippet = XMLFile(FilePath("TrackerDash/snippets/base_content.xml"))
        return content_snippet.load()
