"""
navbar element
"""
from twisted.web.template import Element, XMLFile, renderer
from twisted.python.filepath import FilePath

from TrackerDash.constants import VERSION, TAG
from TrackerDash.database import common
from TrackerDash.database.mongo_accessor import MongoAccessor


class NavBar(Element):
    """
    logic and rendering for the navbar
    """
    def __init__(self, item_to_display=None, item_type=None):
        super(NavBar, self).__init__()
        self.loader = XMLFile(FilePath("TrackerDash/snippets/navbar.xml"))
        self.item_to_display = item_to_display
        self.item_type = item_type
        self.accessor = MongoAccessor()

    @renderer
    def software_version(self, request, tag):
        """
        get the software_version
        """
        return TAG + ' ' + VERSION

    @renderer
    def showreel_dropdown(self, request, tag):
        showreels = common.get_showreel_names(self.accessor)
        for showreel in showreels:
            showreellink = '../showreel/%s' % showreel
            yield tag.clone().fillSlots(
                showreelName=showreel,
                showreelLink=showreellink)

    @renderer
    def dashboards_dropdown(self, request, tag):
        dashboards = common.get_dashboard_names(self.accessor)
        for dashboard in dashboards:
            dashlink = "../dash/%s" % dashboard
            yield tag.clone().fillSlots(dashName=dashboard, dashLink=dashlink)

    @renderer
    def graphs_dropdown(self, request, tag):
        graph_names = common.get_graph_names(self.accessor)
        for graph in graph_names:
            graphlink = "../graph/%s" % graph
            yield tag.clone().fillSlots(graphName=graph, graphLink=graphlink)

    @renderer
    def display_link(self, request, tag):
        """
        display link header button
        """
        if self.item_type == 'dashboard':
            link = "../display/dashboard/%s" % self.item_to_display
        elif self.item_type == 'graph':
            link = "../display/graph/%s" % self.item_to_display
        else:
            link = '../display/showreel/%s' % self.item_to_display
        yield tag.clone().fillSlots(displayLink=link)
