import re
from datetime import datetime

import requests
import lxml.html

from tvshowhelper.informationscrapers import google
from tvshowhelper.informationscrapers import random_useragent
from tvshowhelper.classes.episode import Episode
from tvshowhelper.classes.season import Season
from tvshowhelper.classes.show import Show


def getshow(showname):
    if not isinstance(showname, str):
        raise TypeError("showname must be a string")
    imdburl = _getimdburl(showname)
    show = Show(name=showname, imdburl=imdburl)
    for season in getseasons(showname, imdburl=imdburl):
        for episode in getepisodes(showname, season.number, imdburl=imdburl):
            season.addepisode(episode)
        show.addseason(season)
    return show


def getnumseasons(showname, imdburl=None):
    return len(getseasons(showname, imdburl))


def getseasons(showname, imdburl=None):
    if not isinstance(showname, str):
        raise TypeError("showname must be a string")
    episodesurl = _getimdbepisodesurl(showname, imdburl)
    html = _gethtml(episodesurl)
    doc = lxml.html.fromstring(html)
    seasons = []
    for season in doc.cssselect("select#bySeason option"):
        seasons.append(Season(name="", number=season.get('value').strip().zfill(2)))
    return seasons


def getnumepisodes(showname, season, imdburl=None):
    return len(getepisodes(showname, season))


def getepisodes(showname, season, imdburl=None):
    if not isinstance(showname, str):
        raise TypeError("showname must be a string")
    if imdburl is None:
        imdburl = _getimdburl(showname)
    seasonurl = _getimdbseasonurl(showname, season, imdburl)
    html = _gethtml(seasonurl)
    doc = lxml.html.fromstring(html)
    episodes = []
    for episode in doc.cssselect("div.list_item"):
        name = _fixname(episode.cssselect("strong a")[0].get('title'))
        airdate = _fixairdate(episode.cssselect("div.airdate")[0].text_content().strip())
        number = episode.cssselect("meta")[0].get("content")
        description = episode.cssselect("div.item_description")[0].text_content().strip()
        episodes.append(
            Episode(
                name=name,
                number=number,
                airdate=airdate,
                description=description,
                seasonnumber=season,
                showname=showname,
            )
        )
    return episodes


def _getimdburl(showname):
    results = google.query("site:www.imdb.com {}".format(showname))
    return results[0]['link']


def _getimdbepisodesurl(showname, imdburl=None):
    if imdburl is None:
        imdburl = _getimdburl(showname)
    if not imdburl is None and not imdburl.endswith("/"):
        imdburl += "/"
    return "{}episodes".format(imdburl)


def _getimdbseasonurl(showname, season, imdburl=None):
    episodesurl = _getimdbepisodesurl(showname, imdburl)
    if not episodesurl.endswith("/"):
        episodesurl += "/"
    return "{}?season={}".format(episodesurl, season)


def _getimdbid(imdburl):
    res = re.search("(?P<show_id>\w{1,2}\d+)/?$", imdburl)
    return res.group("show_id")


def _gethtml(url):
    html = None
    try:
        html = requests.get(url, headers={'User-Agent': random_useragent()}).text
    except requests.exceptions.ConnectionError:
        raise Exception("Couldn't connect to {}".format(url))
    return html


def _fixname(name):
    res = re.match("Episode #\d+\.\d+", name)
    if res is not None:  # there was a match
        name = None
    return name


def _fixairdate(airdate):
    if not re.match("\w{3}\.? \d+, \d+", airdate):
        return datetime.strptime("Jan. 01, 1990", "%b. %d, %Y")
    try:
        return datetime.strptime(airdate, "%b. %d, %Y")
    except ValueError:
        return datetime.strptime(airdate, "%b %d, %Y")
