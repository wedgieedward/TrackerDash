"""
class for rendering individual graphs
"""
import json
from TrackerDash.database.mongo_accessor import MongoAccessor


class HighChartsDataRenderer(object):

    def __init__(self, graph_document):
        self.graph_document = graph_document
        self.data_source = graph_document["data_source"]
        self.accessor = MongoAccessor()
        # This is an array of documents needed for this class to process later.
        self.relevant_data = self.get_relevant_data_for_graph_type()
        self.dictionary = {}
        self.process()

    def render_as_json(self):
        return json.dumps(self.dictionary)

    def get_relevant_data_for_graph_type(self):
        """
        """


    def process(self):
        """
        process the graph document and relevent data to be able to
        """


a = """
# pie
{chart: {plotBackgroundColor: null,
         plotBorderWidth: null,
         plotShadow: false},
 title: {text: 'Browser market shares at a specific website, 2010'},
 tooltip: {pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'},
 plotOptions: {pie: {allowPointSelect: true,
               cursor: 'pointer'}},
 series: [{type: 'pie',
           name: 'Browser share',
           data: [['Firefox',   45.0],
                  ['IE',       26.8],
                  ['Safari',    8.5],
                  ['Opera',     6.2],
                  ['Others',   0.7]]}
                   ]
}

# bar
{
chart: {
    type: 'bar'
},
title: {
    text: 'Historic World Population by Region'
},
subtitle: {
    text: 'Source: Wikipedia.org'
},
xAxis: {
     categories: ['Africa', 'America', 'Asia', 'Europe', 'Oceania'],
     title: {
         text: null
     }
 },
yAxis: {
    min: 0,
    title: {
        text: 'Population (millions)',
        align: 'high'
    },
    labels: {
        overflow: 'justify'
    }
},
tooltip: {
    valueSuffix: ' millions'
},
plotOptions: {
    bar: {
        dataLabels: {
            enabled: true
        }
    }
},
legend: {
    layout: 'vertical',
    align: 'right',
    verticalAlign: 'top',
    x: -40,
    y: 100,
    floating: true,
    borderWidth: 1,
    backgroundColor: '#FFFFFF',
    shadow: true
},
credits: {
    enabled: false
},
series: [{
    name: 'Year 1800',
    data: [107, 31, 635, 203, 2]
}, {
    name: 'Year 1900',
    data: [133, 156, 947, 408, 6]
}, {
    name: 'Year 2008',
    data: [973, 914, 4054, 732, 34]
}]
});
}
"""
