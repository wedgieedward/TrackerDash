import logging
import os

from TrackerDash.constants import DEFAULT_THEME


def get_configured_themes():
    configured_themes = []
    # go through the file system and work out what themes are configured
    for _dirname, dirnames, _filenames in os.walk('TrackerDash/web/css/custom'):
        # print path to all subdirectories first.
        for subdirname in dirnames:
            if subdirname != 'fonts':
                configured_themes.append(subdirname)
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
    accessor.add_document_to_collection('config', {"config": 'theme', "theme": theme})
