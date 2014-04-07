from twisted.python.filepath import FilePath
from twisted.web.template import Element, XMLFile, XMLString, renderer

from TrackerDash.common import theme_helpers
from TrackerDash.database.mongo_accessor import MongoAccessor


class AppearanceContent(Element):
    """
    """
    def __init__(self):
        super(AppearanceContent, self).__init__()
        self.loader = XMLFile(FilePath("TrackerDash/snippets/configuration.xml"))
        self.accessor = MongoAccessor()

    @renderer
    def header(self, request, tag):
        """
        """
        return "Appearance Settings"

    @renderer
    def configuration_content(self, request, tag):
        """
        """
        output_string = ""
        output_string += "<div>"
        output_string += "<h3>Themes</h3>"
        output_string += '<div class="btn-group">'

        for theme in theme_helpers.get_configured_themes():
            output_string += (
                "<button type=\"button\" onclick=\"setTheme('%s')\" class=\"btn btn-default\">%s</button>" % (
                    theme,
                    theme
                )
            )

        output_string += "</div>"
        output_string += "</div>"
        renderable_string = XMLString(output_string)
        return renderable_string.load()
