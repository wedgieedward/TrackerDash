"""
Graph object
"""
import json

from twisted.web.template import Element, XMLFile, XMLString, renderer
from twisted.python.filepath import FilePath


class Graph(Element):

    def __init__(self, graph_title):
        super(Graph, self).__init__()
        self.loader = XMLFile(FilePath("TrackerDash/snippets/graph.html"))
        self.graph_title = graph_title

    @renderer
    def drawgraph(self, request, tag):
        """
        renderer for drawing the graph
        This is a pain in the ass for not being able to dynamically]
        render js variables...
        """
        xmlstring = XMLString(self.get_formatted_string())
        return xmlstring.load()

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
        string = self.get_string() % (self.graph_title,
                                      self.get_chart_data(),
                                      self.graph_title)
        return string

    def get_string(self):
        """
        must return valid xml
        """
        return ("""
<graphh>
    <script type="text/javascript">
        $(function () {
            $('#%s').highcharts(jQuery.parseJSON(%r));
        });
    </script>
<div id="%s" style="min-width: 310px; height: 200px; margin: 0"></div>
</graphh>
""")

    def _test_get_json(self):
        """
        NOTE:: this is only a temporary method
        delete this and correctly return the json returned by our api for this
        graph based on its title
        TODO: remeber that the keys in this 'json/dict' are not quoted
              its most likely not even json...
        """
        dictionary = {'chart': {'type': 'bar'},
                      'title': {'text': self.graph_title.title()},
                      'subtitle': {'text': 'Description'},
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
                                  'data': [107, 31, 635, 203, 2]},
                                 {'name': 'Year 1900',
                                  'data': [133, 156, 947, 408, 6]},
                                 {'name': 'Year 2008',
                                  'data': [973, 914, 4054, 732, 34]}]}
        return json.dumps(dictionary)
