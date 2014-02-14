"""
template for welcome page
"""
from twisted.web.resource import Resource
from twisted.python.filepath import FilePath


class WelcomePage(Resource):
    """
    Object for base webpage
    """
    path = 'TrackerDash/web/welcome_page.html'
    def __init__(self):
        super(WelcomePage, self).__init__()
        self.loader = XMLFile(FilePath(self.path))
