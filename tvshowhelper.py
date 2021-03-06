#!/usr/bin/python
"""TV Show Helper

Usage:
    tvshowhelper.py <showname>... --watch-next  [-v]
    tvshowhelper.py <showname>... --update  [-v]
    tvshowhelper.py <showname>... --watch <episode>  [-v]
    tvshowhelper.py <showname>... --next-episode  [-v]
    tvshowhelper.py <showname>... --list  [-v]
    tvshowhelper.py <showname>... --mark-watched <episode> [--mark-previous]  [-v]
    tvshowhelper.py <showname>... --mark-unwatched <episode> [--mark-previous]  [-v]
    tvshowhelper.py <showname>... --download <episode>  [-v]
    tvshowhelper.py <showname>... --download-next <number>  [-v]
    tvshowhelper.py [<filename>...] --rename  [-v]
    tvshowhelper.py --new-episodes  [-v]

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
    --verbose -v                    Verbose logging
"""

from os import listdir

from docopt import docopt

from tvshowhelper.serieswatcher import watchepisode
from tvshowhelper.seriesnamehandler import getepisodeinfo, getshowname
from tvshowhelper.seriescache import SeriesCache
from tvshowhelper.seriesdownloader import downloadepisode
from tvshowhelper.seriesrenamer import renameepisode
from tvshowhelper.askuser import yesno
from tvshowhelper.logger import logger, setlevel as setlogginglevel


def main(args):
    cache = SeriesCache()
    if args.get('--verbose', False):
        setlogginglevel('debug')
    logger.debug("Arguments: {args}".format(args=args))
    if args.get('<showname>', False):
        showname = getshowname(" ".join(args['<showname>']))
        if showname is None:
            print("Couldn't find a show by the name '{n}' "
                  "in your regexes!".format(n=" ".join(args['<showname>'])))
            return
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
    elif args.get('--rename', False):
        rename(cache, args.get('<filename>', []))
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
    askwatchnext(showname, cache)


def watch(showname, cache, episodestring):
    logger.info("watch({name}, {epstring})".format(name=showname, epstring=episodestring))
    seasonnum, episodenum = getepisodeinfo(episodestring)
    assert(seasonnum is not None and episodenum is not None)
    episode = cache.getepisode(showname, seasonnum, episodenum)
    if watchepisode(episode):
        cache.markwatched(episode)
    askwatchnext(showname, cache)


def nextepisode(showname, cache):
    logger.info("nextepisode")
    episode = cache.getnextepisode(showname)
    if episode is None:
        print "No episode found!"
        return
    print("Next episode is: {episode}: {date}".format(episode=episode.getprettyname(),
                                                      date=episode.getairdatestr()).encode('utf8'))


def markwatched(showname, cache, episodestring, markprevious, watched):
    logger.info("markwatched")
    # shortcut so that you don't need to know the name of the next episode.
    if episodestring == "next":
        episode = cache.getnextepisode(showname)
    else:
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
    # user didn't give an argument. he wants to run it on all files in folder.
    if filenames == []:
        filenames = listdir('.')
    for filename in filenames:
        renameepisode(filename, cache=cache)


def update(showname, cache):
    logger.info("update")
    print("Updating {name}..".format(name=showname))
    cache.getshow(showname, update=True)

def askwatchnext(showname, cache):
    if yesno("Would you like to watch the next episode?"):
        watchnext(showname, cache)


if __name__ == '__main__':
    args = docopt(__doc__, version='Series everything v 0.1')
    try:
        main(args)
    except (KeyboardInterrupt, SystemExit):
        print("\nProgram stopped...")
