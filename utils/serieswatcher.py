#!/usr/bin/python
"""Series watcher

Usage:
  serieswatcher.py <showname>... [--update]
  serieswatcher.py <showname>... [--update] [--next-episode]
  serieswatcher.py <showname>... [--update] [--mark-watched=<episode>] [--unwatched] [--mark-previous]

Options:
  -h --help                 Show this screen.
  --next-episode            Display next episode's information
  --mark-watched=<episode>  Episode info (e.g. S01E05).
  --unwatched               Mark as unwatched [default: False].
  --mark-previous           Mark all previous episodes watched as well [default: False].
  --update                  Force an update of the series cache (NOT IMPLEMENTED YET)
"""

import sys
import os
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(ROOT_DIR)
import os
import re

from docopt import docopt

from seriescache import SeriesCache
from seriesrenamer import getepisodeinfo, findshow
import seriesdownloader
import settings as conf
import askuser


def watchnext(showname, update=False):
    cache = SeriesCache()
    regex = findshow(showname)
    if regex is None:
        print "No show by that name!"
        return
    showname, season, episode = getnextepisode(showname, cache, update=update)

    if watch(showname, season.number, episode.number):
        if askuser.yesno("Should the episode be marked as watched?"):
            markwatched(showname, season.number, episode.number, cache)


def watch(showname, seasonnumber, episodenumber):
    showpath = os.path.join(conf.SERIES_ROOT_FOLDER, showname)
    if not os.path.exists(showpath):
        os.mkdir(showpath)
    for filename in os.listdir(showpath):
        seasonnumbertmp, episodenumbertmp = getepisodeinfo(filename)
        if seasonnumbertmp is None or episodenumbertmp is None:
            continue
        if (int(seasonnumber) == int(seasonnumbertmp) and
                int(episodenumber) == int(episodenumbertmp)):
            episodepath = os.path.join(showpath, filename)
            if os.path.exists(episodepath):
                print "Starting {}".format(filename)
                os.system("{} {}".format(conf.VIDEO_COMMAND, episodepath.replace(" ", "\ ")))
                return True
    regex = findshow(showname)
    showname = regex.showname
    cache = SeriesCache()
    episode = cache.getepisode(showname, seasonnumber, episodenumber)
    # if episode is not None:
    #     if datetime.strptime(re.sub('[\.,]', '', episode.getairdate()), "%b %d %Y") > datetime.now():
    #         print "{} S{}E{} hasn't aired yet! It will air {}".format(showname, seasonnumber, episodenumber, episode.getairdate())
    #         return False
    question = "{} S{}E{} - {} wasn't found. Should we try to download it?".format(showname, seasonnumber, episodenumber, episode.name)
    if askuser.yesno(question):
        seriesdownloader.downloadshow(showname, seasonnumber, episodenumber)
        # use watchdog to perform surveillance
        # wait until there is a (video) file in downloads folder that matches the show and episode information.
        # wait until the file has been downloaded.
        # run seriesrenamer on it. then play a sound and ask user if he wants to play the file.


def getnextepisode(showname, cache=None, update=False):
    if cache is None:
        cache = SeriesCache()
    regex = findshow(showname)
    showname = regex.showname
    show = cache.getshow(showname, update=update)
    nextepisode = None
    nextseason = None
    for season in show.seasons:
        for episode in season.episodes:
            if episode.watched:
                continue
            if nextepisode is None:
                nextepisode = episode
            if nextseason is None:
                nextseason = season
            if (int(season.number) < int(nextseason.number) or
                    int(season.number) == int(nextseason.number) and
                    int(episode.number) < int(nextepisode.number)):
                nextepisode = episode
                nextseason = season

    return showname, nextseason, nextepisode


def markwatched(showname, seasonnumber, episodenumber, markprevious=False, watched=True, cache=None):
    if cache is None:
        cache = SeriesCache()
    cache = SeriesCache()
    regex = findshow(showname)
    showname = regex.showname
    show = cache.getshow(showname)
    if markprevious:
        _markpreviouswatched(show, seasonnumber, episodenumber, watched=watched)
    else:
        _markwatched(show, seasonnumber, episodenumber, watched=watched)
    cache.saveshow(show)


def _markpreviouswatched(show, seasonnumber, episodenumber, watched=True):
    for season in show.seasons:
        if int(season.number) < int(seasonnumber):
            for episode in season.episodes:
                    episode.watched = watched
        elif int(season.number) == int(seasonnumber):
            for episode in season.episodes:
                if int(episode.number) <= int(episodenumber):
                    episode.watched = watched


def _markwatched(show, seasonnumber, episodenumber, watched=True):
    season = show.getseason(seasonnumber)
    if season is not None:
        episode = season.getepisode(episodenumber)
        if episode is not None:
            episode.watched = watched


if __name__ == '__main__':
    arguments = docopt(__doc__, version='Series watcher v1.0')

    cache = SeriesCache()
    showname = arguments['<showname>']
    if type(showname) is list:
        showname = " ".join(showname)

    if arguments['--next-episode']:
        showname, season, episode = getnextepisode(showname=showname, cache=cache, update=arguments['--update'])
        if None in [season, episode]:
            print "There are no more episodes in the cache! Try updating with the --update argument"
            sys.exit(0)
        print "Next episode of {} is: S{}E{} (airdate {})".format(showname, season.number, episode.number, episode.getairdate())
        sys.exit(0)

    if arguments['--mark-watched']:
        episode = arguments['--mark-watched'].lower()
        if not re.match('s\d+e\d+', episode):
            print "Incorrect arguments for --mark-watched"
            sys.exit(0)
        seasonnumber, episodenumber = episode[1:].split('e')
        markwatched(showname, seasonnumber=seasonnumber,
                    episodenumber=episodenumber, markprevious=arguments['--mark-previous'],
                    watched=(not arguments['--unwatched']), cache=cache)
        sys.exit(0)
    watchnext(showname, update=arguments['--update'])
