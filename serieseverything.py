#!/usr/bin/python
"""Series everything

Usage:
  serieseverything.py <showname>... --watch-next
  serieseverything.py <showname>... --update
  serieseverything.py <showname>... --watch <episode>
  serieseverything.py <showname>... --next-episode
  serieseverything.py <showname>... --list
  serieseverything.py <showname>... --mark-watched <episode> [--mark-previous]
  serieseverything.py <showname>... --download <episode>

Options:
  -h --help                     Show this screen.
  --watch-next                  Watch next episode.
  --watch <episode>             Watch specific episode (e.g. s01e05).
  --next-episode                Display next episode's information, e.g. 's01e05 - title (release date)'.
  --mark-watched <episode>      Episode info (e.g. s01e05). See mark-previous option.
  --mark-unwatched <episode>    Episode info (e.g. s01e05). See mark-previous option.
  --mark-previous               Mark all previous episodes watched as well as the one specified [default: False].
  --download <episode>          Download episode (e.g. s01e05).
  --download-next               Download episode (e.g. s01e05).
  --update                      Force an update of the series cache.
"""

from datetime import datetime

from docopt import docopt

from utils.serieswatcher import watch
from utils.seriesnamehandler import getepisodeinfo, getshowname
from utils.seriescache import SeriesCache
from utils.seriesdownloader import downloadshow
from settings import AIR_DATE_FORMAT


def main(args):
    showname = getshowname(" ".join(args['<showname>']))
    cache = SeriesCache()

    markprevious = args.get('--mark-previous', False)

    if args.get('--watch-next', False):
        episode = cache.getnextepisode(showname)
        watch(showname, episode, cache=cache)

    elif args.get('--watch', False):
        seasonnum, episodenum = getepisodeinfo(args['--watch'])
        episode = cache.getepisode(showname, seasonnum, episodenum)
        watch(showname, episode, cache=cache)

    elif args.get('--next-episode', False):
        episode = cache.getnextepisode(showname)
        epname = episode.getprettyname(showname=showname)
        print "Next episode is: {} ({})".format(epname, datetime.strftime(episode.airdate, AIR_DATE_FORMAT))

    elif args.get('--mark-watched', False):
        seasonnum, episodenum = getepisodeinfo(args['--mark-watched'])
        episode = cache.getepisode(showname, seasonnum, episodenum)
        cache.markwatched(showname, episode, markprevious=markprevious, watched=True)

    elif args.get('--mark-unwatched', False):
        season, episode = getepisodeinfo(args['--mark-unwatched'])
        cache.markwatched(showname, episode, markprevious=markprevious, watched=False)

    elif args.get('--download', False):
        seasonnum, episodenum = getepisodeinfo(args['--download'])
        downloadshow(showname, seasonnum, episodenum)

if __name__ == '__main__':
    args = docopt(__doc__, version='Series everything v 0.1')
    main(args)
