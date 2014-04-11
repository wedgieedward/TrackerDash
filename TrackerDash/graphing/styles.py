"""
styles constants
"""


def mergedicts(dict1, dict2):
    """
    http://stackoverflow.com/questions/7204805/
    python-dictionaries-of-dictionaries-merge
    """
    for k in set(dict1.keys()).union(dict2.keys()):
        if k in dict1 and k in dict2:
            yield (k, dict(mergedicts(dict1[k], dict2[k])))
        elif k in dict1:
            yield (k, dict1[k])
        else:
            yield (k, dict2[k])


BASE_STYLE = {
    'plotOptions': {
        'bar': {
            'dataLabels': {
                'enabled': True
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
            "size": '90%'
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
        "allowDecimals": False,
        "opposite": True,
        "labels": {
            "style": {
                "font": 'Helvetica',
                "fontWeight": 'bold',
                "fontSize": '14px',
                'color': 'white'
            }
        }
    }

}

LIGHT_STYLE = {
    "title": {'color': 'black'},
    "subtitle": {'color': 'black'},
    'xAxis': {'labels': {'style': {'color': 'black'}}},
    'yAxis': {"labels": {"style": {'color': 'black'}}},
    'legend': {"itemStyle": {"color": "black"}},

}

DARK_STYLE = {
    "title": {'color': 'white'},
    "subtitle": {'color': 'white'},
    'xAxis': {'labels': {'style': {'color': 'white'}}},
    'yAxis': {"labels": {"style": {'color': 'white'}}},
    'legend': {"itemStyle": {"color": "white"}},
}

STYLES = {
    'light': mergedicts(BASE_STYLE, LIGHT_STYLE),
    'dark': mergedicts(BASE_STYLE, DARK_STYLE)
}


def get_style_dict(style):
    return STYLES.get(style, None)
