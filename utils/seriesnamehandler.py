import os

from settings import (SEASON_EPISODE_REGEX, SEASON_EPISODE_REGEX_EXTRAS, SERIES_ROOT_FOLDER,
                               SERIES_DOWNLOAD_FOLDER, SEARCH_DOWNLOAD_FOLDER)
from settings.regexes import SERIES_REGEXES
import askuser


def getepisodeinfo(txt):
    res = SEASON_EPISODE_REGEX.search(txt)
    if res is not None:
        ep = _regex(res)
        return ep[0], ep[1]

    regexmatches = []
    for regex in SEASON_EPISODE_REGEX_EXTRAS:
        res = regex.search(txt)
        if res is None:
            continue
        ep = _regex(res)
        epinfo = "S{}E{}".format(ep[0], ep[1])
        regexmatches.append((epinfo, res))
    if regexmatches == []:
        return None, None

    option = askuser.multipleoptions("Which episode numbering is correct? ({})".format(txt),
                                     regexmatches, lambda x: x[0])
    if option is None:
        return None, None
    ep = _regex(option[1])
    return ep[0], ep[1]


def getshowname(txt):
    matches = _findshowmatches(txt)
    if len(matches) == 1:
        match = matches[0]
    elif len(matches) > 1:
        question = "\nWhich show does \"{}\" belong to?".format(txt)
        match = askuser.multipleoptions(question, matches, lambda x: x.showname)
    else:
        match = None
    return match.showname


def getepisodepath(showname, episode):
    showpath = os.path.join(SERIES_ROOT_FOLDER, showname)

    searchdirs = [showpath]
    if SEARCH_DOWNLOAD_FOLDER:
        searchdirs.append(SERIES_DOWNLOAD_FOLDER)
    for searchdir in searchdirs:
        if not os.path.exists(searchdir):
            continue
        for filename in os.listdir(searchdir):  # perhaps do listdir with predefined file-extensions? mp4, mkv, avi
            seasonnumtmp, episodenumtmp = getepisodeinfo(filename)
            if seasonnumtmp is None or episodenumtmp is None:
                continue
            if (episode.seasonnumber == seasonnumtmp and episode.number == episodenumtmp):
                return os.path.join(searchdir, filename)
    return None


def _findshowmatches(txt):
    matches = []
    for regex in SERIES_REGEXES:
        if regex.regex.search(txt):
            matches.append(regex)
    return matches


def _regex(match):
    """ Return tuple of zero-filled season and episode numbers.
    """
    return (match.group('season').zfill(2), match.group('episode').zfill(2))
