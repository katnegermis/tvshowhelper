#!/usr/bin/python

import sys
sys.path.append("/media/storage/Dropbox/Koding/python/series_everything")

from downloadscrapers import filestube
from downloaders import jdownloader
from seriescache import SeriesCache
import askuser


def download(query, start=False):
    links = filestube.getlinks(query)
    link = askuser.multipleoptions("Which file should we download?", links, lambda x: x.gettitle())
    if link is None:
        print "No link chosen"
        return
    jdownloader.download(link, start)


def downloadshow(showname, seasonnumber=None, episodenumber=None, start=False):
    cache = SeriesCache()
    if seasonnumber is None and episodenumber is None:
        _downloadshow(cache, showname, start)
    elif seasonnumber is not None and episodenumber is None:
        _downloadseason(cache, showname, seasonnumber, start)
    elif seasonnumber is not None and episodenumber is not None:
        _downloadepisode(showname, seasonnumber, episodenumber, start)
    else:
        print "Error"


def _downloadshow(cache, showname, start):
    cache.getshow(showname)
    show = cache.getshow(showname)
    for season in show.getseasons():
        _downloadseason(cache, showname, season.getnumber(), start)


def _downloadseason(cache, showname, seasonnumber, start):
    seasonnumber = str(seasonnumber).zfill(2)
    season = cache.getseason(showname, seasonnumber)
    for episode in season.getepisodes():
        _downloadepisode(showname, seasonnumber, episode.getnumber(), start)


def _downloadepisode(showname, seasonnumber, episodenumber, start):
    episodenumber = str(episodenumber).zfill(2)
    query = "{} S{}E{}".format(showname, seasonnumber, episodenumber)
    download(query, start=start)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        download(" ".join(sys.argv[1:]))
    else:
        downloadshow("Two and a Half Men", seasonnumber=10)
