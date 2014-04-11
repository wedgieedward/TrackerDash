import logging
import os

from TrackerDash.constants import DEFAULT_THEME
from TrackerDash.constants import DEFAULT_STYLE


def get_configured_themes():
    configured_themes = []
    # go through the file system and work out what themes are configured
    for _dirname, dirnames, _filenames in os.walk(
            'TrackerDash/web/css/custom'):
        # print path to all subdirectories first.
        for subdirname in dirnames:
            if subdirname != 'fonts':
                configured_themes.append(subdirname)
    configured_themes.sort()
    return configured_themes


def get_default_theme():
    """
    get the default theme
    """
    return DEFAULT_THEME


def set_theme(accessor, theme):
    """
    set a theme
    """
    logging.info("Setting application theme: %s" % theme)
    accessor.remove_documents_by_query('config', {"config": "theme"})
    accessor.add_document_to_collection(
        'config', {"config": 'theme', "theme": theme})


def get_configured_theme(accessor):
    """
    go to the configuration and get the saved theme
    """
    theme_document = accessor.get_one_document_by_query(
        'config', {'config': 'theme'})
    if theme_document is None:
        logging.info("No theme found, adding default theme")
        theme = get_default_theme()
        set_theme(accessor, theme)
    else:
        theme = theme_document["theme"]
    return theme


def get_configured_style(accessor):
    """
    get the configured graph style
    """
    style_document = accessor.get_one_document_by_query(
        'config', {'config': 'style'})
    if style_document is None:
        logging.info("No graph style found, setting default style")
        style = get_default_style()
        set_style(accessor, style)
    else:
        style = style_document["style"]
    return style


def get_default_style():
    return DEFAULT_STYLE


def get_configured_styles():
    return ('light', 'dark')


def set_style(accessor, style):
    """
    set a style to the configuration table
    """
    logging.info("Setting application style: %s" % style)
    accessor.remove_documents_by_query('config', {"config": "style"})
    accessor.add_document_to_collection(
        'config', {"config": 'style', "style": style})
