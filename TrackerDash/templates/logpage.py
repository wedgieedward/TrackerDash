from twisted.web.template import XMLFile, renderer, XMLString
from twisted.python.filepath import FilePath
from basewebpage import BasePage


class LogPage(BasePage):
    """
    LogPage
    """
    DEFAULT_TAG = XMLString('<span class="label label-default"> Log </span>')
    INFO_TAG = XMLString('<span class="label label-info">Info</span>')
    DEBUG_TAG = XMLString('<span class="label label-warning">Debug</span>')
    PRIMARY_TAG = XMLString('<span class="label label-primary">Primary</span>')
    SUCCESS_TAG = XMLString('<span class="label label-success">Success</span>')
    DANGER_TAG = XMLString('<span class="label label-danger">Danger</span>')

    def __init__(self, log_file, title):
        self.log_file = log_file
        self.title = title
        super(LogPage, self).__init__()

    @renderer
    def content(self, request, tag):
        """
        get the content for the configuration page
        """
        log_content = XMLFile(FilePath("TrackerDash/snippets/logs.xml"))
        return log_content.load()

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
            log_type = self.get_log_label(log_line)
            yield tag.clone().fillSlots(log_line=log_line, log_label=log_type.load())

    def get_log_file_contents(self):
        """
        open the log file, return an list of all the log lines in reverse order
        """
        log_file = open(self.log_file, 'r')
        lines = log_file.readlines()
        # TODO remove this when log rotation is properly implemented
        lines = lines[-100:]  # Get the last 100 lines
        log_file.close()
        lines.reverse()  # Put them in a displayable order
        return lines

    def get_log_label(self, log_line):
        """
        """
        label = self.DEFAULT_TAG
        if "INFO" in log_line:
            label = self.INFO_TAG
        elif "DEBUG" in log_line:
            label = self.DEBUG_TAG
        elif "200" in log_line or "304" in log_line:
            label = self.SUCCESS_TAG
        elif "404" in log_line or "500" in log_line:
            label = self.DANGER_TAG
        return label
