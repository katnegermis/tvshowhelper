#!/usr/bin/python
"""Series everything

Usage:
    serieseverything.py <showname>... --watch-next
    serieseverything.py <showname>... --update
    serieseverything.py <showname>... --watch <episode>
    serieseverything.py <showname>... --next-episode
    serieseverything.py <showname>... --list
    serieseverything.py <showname>... --mark-watched <episode> [--mark-previous]
    serieseverything.py <showname>... --mark-unwatched <episode> [--mark-previous]
    serieseverything.py <showname>... --download <episode>
    serieseverything.py <showname>... --download-next <number>
    serieseverything.py <filename>... --rename
    serieseverything.py --new-episodes

Options:
    --help -h                       Show this screen.
    --watch-next -w                 Watch next episode.
    --watch <episode>               Watch specific episode (e.g. s01e05).
    --next-episode -n               Display next episode's information, e.g. 's01e05 - title (release date)'.
    --mark-watched <episode> -m     Episode info (e.g. s01e05). See mark-previous option.
    --mark-unwatched <episode> -u   Episode info (e.g. s01e05). See mark-previous option.
    --mark-previous -p              Mark all previous episodes watched as well as the one specified [default: False].
    --download <episode> -d         Download episode (e.g. s01e05).
    --download-next                 Download episode (e.g. s01e05) [default: 1].
    --update -u                     Force an update of the series cache.
    --new-episodes                  List recently aired, unwatched episodes.
    --rename -r                     Rename file [default: 'all'].
"""

from os import listdir

from docopt import docopt

from tvshowhelper.serieswatcher import watchepisode
from tvshowhelper.seriesnamehandler import getepisodeinfo, getshowname
from tvshowhelper.seriescache import SeriesCache
from tvshowhelper.seriesdownloader import downloadepisode
from tvshowhelper.seriesrenamer import renameepisode
from tvshowhelper.askuser import yesno
from tvshowhelper import logger


def main(args):
    cache = SeriesCache()
    logger.debug("Arguments: {args}".format(args=args))
    if args.get('<showname>', False):
        showname = getshowname(" ".join(args['<showname>']))
        logger.info("Showname: '{name}'".format(name=showname))

    if args.get('--watch-next', False):
        watchnext(showname, cache)
    elif args.get('--watch', False):
        watch(showname, cache, args['--watch'])
    elif args.get('--next-episode', False):
        nextepisode(showname, cache)
    elif args.get('--mark-watched', False):
        markwatched(showname, cache, args['--mark-watched'], watched=True,
                    markprevious=args.get('--mark-previous', False))
    elif args.get('--mark-unwatched', False):
        markwatched(showname, cache, args['--mark-unwatched'], watched=False,
                    markprevious=args.get('--mark-previous', False))
    elif args.get('--download', False):
        download(showname, cache)
    elif args.get('--update', False):
        update(showname, cache)
    elif args.get('--rename', False) and args.get('<filename>', False):
        rename(cache, args['<filename>'])
    else:
        print('Unimplemented/unknown arguments "{}".'.format(args))


def watchnext(showname, cache):
    logger.info("watchnext")
    episode = cache.getnextepisode(showname)
    if episode is None:
        print("Couldn't find any new episodes!")
        if yesno("Would you like to update the cache?"):
            update(showname, cache)
            watchnext(showname, cache)  # this could be an endless loop.
        return
    if watchepisode(episode):
        cache.markwatched(episode)


def watch(showname, cache, episodestring):
    logger.info("watch({name}, {epstring})".format(name=showname, epstring=episodestring))
    seasonnum, episodenum = getepisodeinfo(episodestring)
    assert(seasonnum is not None and episodenum is not None)
    episode = cache.getepisode(showname, seasonnum, episodenum)
    if watchepisode(episode):
        cache.markwatched(episode)


def nextepisode(showname, cache):
    logger.info("nextepisode")
    episode = cache.getnextepisode(showname)
    print("Next episode is: {} ({}): {}".format(episode.getprettyname(),
                                                episode.getairdatestr()).encode('utf8'))


def markwatched(showname, cache, episodestring, markprevious, watched):
    logger.info("markwatched")
    seasonnum, episodenum = getepisodeinfo(episodestring)
    episode = cache.getepisode(showname, seasonnum, episodenum)
    cache.markwatched(episode, markprevious=markprevious, watched=watched)


def download(showname, cache):
    logger.info("download")
    seasonnum, episodenum = getepisodeinfo(args['--download'])
    episode = cache.getepisode(showname, seasonnum, episodenum)
    downloadepisode(episode)


def rename(cache, filenames):
    logger.info("rename")
    if not isinstance(filenames, list) and filenames.lower() == "all":
        filenames = listdir('.')
    for filename in filenames:
        renameepisode(filename, cache=cache)


def update(showname, cache):
    logger.info("update")
    print("Updating {name}..".format(name=showname))
    cache.getshow(showname, update=True)


if __name__ == '__main__':
    args = docopt(__doc__, version='Series everything v 0.1')
    main(args)
