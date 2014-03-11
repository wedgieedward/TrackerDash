"""
Graph object
"""
import json
import random


class Graph(object):

    def __init__(self, graph_title, graph_description, data_source, row_span, number_of_rows):
        super(Graph, self).__init__()
        self.graph_title = graph_title
        self.graph_description = graph_description
        self.data_source = data_source
        self.row_span = row_span
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
        returns a dict that highcharts.js can render correctly
        """
        return self._test_get_json()

    def get_formatted_string(self):
        """
        get_string returns a string that needs .format()
        to be applied to it to be valid
        """
        string = self.get_string() % (self.number_of_rows,
                                      self.row_span,
                                      self.data_source,
                                      self.data_source,
                                      self.get_chart_data(),
                                      self.data_source)
        return string

    def get_string(self):
        """
        must return valid xml
        """
        return ("""
<div>
    <script type="text/javascript">
        $(document).ready(function () {
            win_height = $(window).height();
            top_nav_bar_height = $("#top_nav_bar").height();
            bottom_nav_bar_height = $("#bottom_nav_bar").height();
            offset = 0;
            num_rows = %d;
            span_rows = %d;
            if (top_nav_bar_height != null){
                offset = top_nav_bar_height + bottom_nav_bar_height;
            }
            height = ((win_height - offset) / num_rows) * span_rows;
            $("#%s").css({"height": height.toString()+"px"});
            $('#%s').highcharts(jQuery.parseJSON(%r));
        });
    </script>
<div id="%s" style="min-width: 310px; margin: 0"></div>
</div>
""")

    def _test_get_json(self):
        """
        NOTE:: this is only a temporary method
        delete this and correctly return the json returned by our api for this
        graph based on its title either in this class or at page load time in
        the javascript
        """
        dictionary = {'chart': {'type': random.choice(['line',
                                                       'bar',
                                                       'area',
                                                       'column',
                                                       'scatter'])},
                      'title': {'text': self.graph_title.title()},
                      'subtitle': {'text': self.graph_description},
                      'xAxis': {'categories': ['Africa', 'America', 'Asia', 'Europe', 'Oceania'],
                                'title': {'text': None}},
                      'yAxis': {'min': 0,
                                'title': {'text': 'Population (millions)',
                                          'align': 'high'},
                                'labels': {'overflow': 'justify'}
                                },
                      'tooltip': {'valueSuffix': ' millions'},
                      'plotOptions': {'bar': {'dataLabels': {'enabled': True}}},
                      'legend': {'layout': 'vertical',
                                 'align': 'right',
                                 'verticalAlign': 'top',
                                 'x': -40,
                                 'y': 100,
                                 'floating': True,
                                 'borderWidth': 1,
                                 'backgroundColor': '#FFFFFF',
                                 'shadow': True
                                 },
                      'credits': {'enabled': False},
                      'series': [{'name': 'Year 1800',
                                  'data': [random.randint(0, 1000) for r in range(5)]},
                                 {'name': 'Year 1900',
                                  'data': [random.randint(0, 1000) for r in range(5)]},
                                 {'name': 'Year 2008',
                                  'data': [random.randint(0, 1000) for r in range(5)]}]}
        return json.dumps(dictionary)
