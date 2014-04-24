"""
graph container element
"""
import json
import logging

from twisted.web.template import Element, XMLFile, renderer, XMLString
from twisted.python.filepath import FilePath

from TrackerDash.database.mongo_accessor import MongoAccessor


class ShowreelContent(Element):
    """
    Element to handle the content of a dashboard page
    """

    def __init__(self, showreel_name, display=False):
        super(ShowreelContent, self).__init__()
        self.loader = XMLFile(
            FilePath("TrackerDash/snippets/graphcontent.xml"))
        self.showreel_name = showreel_name
        self.display = display
        self.accessor = MongoAccessor()
        self.showreel_document = self.accessor.get_one_document_by_query(
            "showreel",
            {"title": self.showreel_name})
        logging.debug("Showreel Document: %r" % self.showreel_document)

    @renderer
    def render_content(self, request, tag):
        """
        render the content for the graph container
        """
        if self.showreel_document is not None:
            graph_row_xml = XMLString(self.get_content_xml())
            return graph_row_xml.load()
        else:
            oops_container = self.get_bad_container()
            return oops_container.load()

    def get_bad_container(self):
        """
        something has gone wrong that causes the page not to render correctly
        return some xml to respond to this
        """
        return XMLFile(
            FilePath("TrackerDash/snippets/no_dash_data_container.xml"))

    def get_content_xml(self):
        """
        """
        xml = "<div>"
        xml += '<div class="row clearfix">'
        url_list = self.get_showreel_item_urls()
        if len(url_list) == 0:
            oops_container = self.get_bad_container()
            xml += oops_container.load()
        else:
            xml += """
            <iframe
            id="show_reel_pane"
            width="100%%"
            height="100%%"
            frameBorder="0"
            style="overflow: hidden; border-radius: 0px;"
            class="container col-md-12">
            </iframe>
                    <script>
                        (function() {
                            var e = document.getElementById('show_reel_pane'),
                                f = function( el, url ) {
                                    el.src = url;
                                },
                                urls = [%s],
                                i = 0,
                                l = urls.length;

                                (function rotation() {
                                    if ( i != l-1 ) {
                                        i++
                                    } else {
                                        i = 0;
                                    }
                                    f( e, urls[i] );
                                    setTimeout( arguments.callee, 1000 * %s);
                                })();
                        })();
                    </script>
                    """ % (' ,'.join(url_list),
                           self.showreel_document["refresh_interval"])

        xml += '</div>'
        xml += "</div>"
        return xml

    def get_showreel_item_urls(self):
        """
        get the showreel item url array
        """

        links = []
        rel_path = "../"
        if self.display:
            rel_path = rel_path * 2
        for item in self.showreel_document["reels"]:
            if item["item_type"] == 'dashboard':
                link = "../%sdisplay/dashboard/%s" % (rel_path, item["title"])
                links.append(json.dumps(link))
            elif item["item_type"] == 'graph':
                link = "../%sdisplay/graph/%s" % (rel_path, item["title"])
                links.append(json.dumps(link))

        return links
