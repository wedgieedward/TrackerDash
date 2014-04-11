"""
Graph object
"""
import uuid

from TrackerDash.graphing.graph_constructor import HighchartsConstructor


class HighchartsGraph(object):

    def __init__(self, graph_document, number_of_rows):
        self.graph_document = graph_document
        self.graph_title = graph_document["title"]
        self.graph_description = graph_document["description"]
        self.unique_ref = uuid.uuid4()
        self.row_span = graph_document["height"]
        self.number_of_rows = number_of_rows

    def load(self):
        """
        renderer for drawing the graph
        This is a pain in the ass for not being able to dynamically]
        render js variables...
        """
        return self.get_formatted_string()

    def get_chart_data(self):
        """
        creates a HighChartsDataRenderer and renders it as json
        """
        constructor = HighchartsConstructor(self.graph_document)
        return constructor.render_as_json()

    def get_formatted_string(self):
        """
        get_render_script returns a string that needs .format()
        to be applied to it to be valid
        """
        string = self.get_render_script() % (
            self.number_of_rows,
            self.row_span,
            self.unique_ref,
            self.unique_ref,
            self.get_chart_data(),
            self.unique_ref)

        return string

    def get_render_script(self):
        """
        returns the javascript needed to render this particular chart
        """
        return (
            """
            <div>
                <script type="text/javascript">
                    $(document).ready(function () {
                        win_height = $(window).height();
                        top_nav_bar_height = $("#top_nav_bar").height();
                        bottom_nav_bar_height = $("#bottom_nav_bar").height();
                        offset = 0;
                        fudge_padding = 20;
                        num_rows = %d;
                        span_rows = %d;
                        if (top_nav_bar_height != null){
                            offset = top_nav_bar_height + bottom_nav_bar_height;
                        }
                        height = ((win_height - offset - fudge_padding) / num_rows) * span_rows;
                        $("#%s").css({"height": height.toString()+"px"});
                        $('#%s').highcharts(jQuery.parseJSON(%r));
                    });
                </script>
            <div id="%s" style="min-width: 310px; margin: 0"></div>
            </div>
            """)
