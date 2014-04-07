import os


def get_configured_themes():
    configured_themes = []
    # go through the file system and work out what themes are configured
    for _dirname, dirnames, _filenames in os.walk('../web/css/custom'):
        # print path to all subdirectories first.
        for subdirname in dirnames:
            if subdirname != 'fonts':
                configured_themes.append(subdirname)
    return configured_themes

if __name__ == '__main__':
    print get_configured_themes()
