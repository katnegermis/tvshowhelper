#!/usr/bin/python

import sys
import os
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(ROOT_DIR)

from downloaders import jdownloader
from seriescache import SeriesCache
from settings import DOWNLOADERS
import askuser
from importer import doimport, modulejoin

DOWNLOADSCRAPERS_MODULE = modulejoin("utils", "downloadscrapers")
DOWNLOADERS_MODULE = modulejoin("utils", "downloaders")

def download(query, start=False):
    if len(DOWNLOADERS) == 1:
        downloadtype = DOWNLOADERS[0]
    else:
        downloadtype = askuser.multipleoptions("Which downloader would you like to use?", DOWNLOADERS, lambda x: x['downloader'])
    if downloadtype is None:
        return False

    if len(downloadtype['scrapers']) == 1:
        scrapermodule = modulejoin(DOWNLOADSCRAPERS_MODULE, downloadtype['scrapers'][0], downloadtype['scrapers'][0].capitalize())
    else:
        scrapertype = askuser.multipleoptions("Which download scraper would you like to use?", downloadtype['scrapers'])
        scrapermodule = modulejoin(DOWNLOADSCRAPERS_MODULE, scrapertype, scrapertype.capitalize())

    Scrapercls = doimport(scrapermodule)
    scraper = Scrapercls()
    links = scraper.getlinks(query)
    print links
    downloadmodule = modulejoin(DOWNLOADERS_MODULE, downloadtype['downloader'], downloadtype['downloader'].capitalize())
    Downloader = doimport(downloadmodule)
    downloader = Downloader()
    print downloader.download(link)

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
    for season in show.seasons:
        _downloadseason(cache, showname, season.number, start)


def _downloadseason(cache, showname, seasonnumber, start):
    seasonnumber = str(seasonnumber).zfill(2)
    season = cache.getseason(showname, seasonnumber)
    for episode in season.episodes:
        _downloadepisode(showname, seasonnumber, episode.number, start)


def _downloadepisode(showname, seasonnumber, episodenumber, start):
    episodenumber = str(episodenumber).zfill(2)
    query = "{} S{}E{}".format(showname, seasonnumber, episodenumber)
    download(query, start=start)
