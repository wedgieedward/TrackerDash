"""
styles constants
"""
from copy import deepcopy


def mergedicts(dictionary1, dictionary2):
    """
    merges merge_dict into main_dict
    """
    output = {}
    for item, value in dictionary1.iteritems():
        if item in dictionary2:
            if isinstance(dictionary2[item], dict):
                output[item] = mergedicts(value, dictionary2.pop(item))
        else:
            output[item] = value
    for item, value in dictionary2.iteritems():
        output[item] = value
    return output


BASE_STYLE = {
    'plotOptions': {
        'bar': {
            'dataLabels': {
                'enabled': True,
                'color': 'white'
            }
        },
        'area': {
            'fillOpacity': 0.5,
            'marker': {
                "enabled": False
            }
        },
        "pie": {
            "allowPointSelect": True,
            "cursor": 'pointer',
            "dataLabels": {
                "distance": -50,
                "enabled": True,
                "inside": True,
                "offset": 0,
                "style": {
                    "font": 'Helvetica',
                    "fontWeight": 'bold',
                    "fontSize": '14px'
                },
                "color": 'white',
                "y": 0,
                "overflow": False,
            },
            "size": '100%'
        },
        "scatter": {
            "marker": {
                "radius": 5,
                "states": {
                    "hover": {
                        "enabled": True,
                        "lineColor": 'rgb(100,100,100)'
                    }
                }
            }
        },
        "line": {
            "marker": {
                "enabled": False
            },
            "lineWidth": 5
        },
    },  # End plot options
    'title': {'fontWeight': 'bold'},
    'chart': {'backgroundColor': 'transparent'},
    'xAxis': {
        "title": {
            "align": "high"
        },
        "labels": {
            "style": {
                'fontWeight': 'bold',
            }
        }
    },
    'yAxis': {
        "title": '',
        "maxPadding": 0,
        "minPadding": 0,
        "allowDecimals": False,
        "opposite": True,
        "labels": {
            "style": {
                "font": 'Helvetica',
                "fontWeight": 'bold',
                "fontSize": '14px',
            }
        }
    }

}

# For a good reference on what colours to use see:
#     http://www.tedmontgomery.com/tutorial/clrspcBL.html


LIGHT_STYLE = {
    "title": {'style': {'color': 'black'}},
    "subtitle": {'style': {'color': 'black'}},
    'xAxis': {
        'labels': {'style': {'color': 'black'}},
        'title': {'style': {'color': 'black'}}
    },
    'yAxis': {"labels": {"style": {'color': 'black'}}},
    'legend': {"itemStyle": {"color": "black"}},
    'labels': {"style": {"color": "black"}},
    # highcharts by default is designed for a white background
}

DARK_STYLE = {
    "title": {'style': {'color': 'white'}},
    "subtitle": {'style': {'color': 'white'}},
    'xAxis': {
        'labels': {'style': {'color': 'white'}},
        'title': {'style': {'color': 'white'}}
    },
    'yAxis': {"labels": {"style": {'color': 'white'}}},
    'legend': {"itemStyle": {"color": "white"}},
    'labels': {"style": {"color": "white"}},
    'colors': [
        "#FF4040",
        "#FF8040",
        "#FFC000",
        "#44FF44",
        "#0040C0",
        "#0080C0",
        "#C00040",
        "#C04080",
        "#00C000",
        "#00C080",
        "#80C080",
        "#4040FF",
        "#4080FF",
        "#C080FF",
    ]
}


def get_style_dict(style):
    if style == 'light':
        return mergedicts(deepcopy(BASE_STYLE), deepcopy(LIGHT_STYLE))
    elif style == 'dark':
        return mergedicts(deepcopy(BASE_STYLE), deepcopy(DARK_STYLE))
    else:
        return deepcopy(BASE_STYLE)
