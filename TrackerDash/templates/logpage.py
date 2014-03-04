from twisted.web.template import XMLFile, renderer
from twisted.python.filepath import FilePath
from basewebpage import BasePage


class LogPage(BasePage):
    """
    LogPage
    """
    def __init__(self, log_file, title):
        self.log_file = log_file
        self.title = title
        super(LogPage, self).__init__()

    @renderer
    def content(self, request, tag):
        """
        get the content for the configuration page
        """
        config_content = XMLFile(FilePath("TrackerDash/snippets/logs.xml"))
        return config_content.load()

    @renderer
    def auto_refresh(self, request, tag):
        """
        render the auto refresh meta tag
        """
        return ""

    @renderer
    def get_title(self, request, tag):
        """
        """
        return self.title

    @renderer
    def get_log_lines(self, request, tag):
        """
        render the log lines
        """
        for log_line in self.get_log_file_contents():
            yield tag.clone().fillSlots(log_line=log_line)

    def get_log_file_contents(self):
        """
        open the log file, return an list of all the log lines in reverse order
        """
        log_file = open(self.log_file, 'r')
        lines = log_file.readlines()
        log_file.close()
        lines.reverse()
        return lines
