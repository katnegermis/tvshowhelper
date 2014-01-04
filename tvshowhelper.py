#!/usr/bin/python
"""Series everything

Usage:
    serieseverything.py <showname>... --watch-next  [-v]
    serieseverything.py <showname>... --update  [-v]
    serieseverything.py <showname>... --watch <episode>  [-v]
    serieseverything.py <showname>... --next-episode  [-v]
    serieseverything.py <showname>... --list  [-v]
    serieseverything.py <showname>... --mark-watched <episode> [--mark-previous]  [-v]
    serieseverything.py <showname>... --mark-unwatched <episode> [--mark-previous]  [-v]
    serieseverything.py <showname>... --download <episode>  [-v]
    serieseverything.py <showname>... --download-next <number>  [-v]
    serieseverything.py [<filename>...] --rename  [-v]
    serieseverything.py --new-episodes  [-v]

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
from tvshowhelper.seriesdownloader import downloadepisode
from tvshowhelper.seriesrenamer import renameepisode
from tvshowhelper.askuser import yesno
from tvshowhelper.logger import logger, setlevel as setlogginglevel


def main(args):
    if args.get('--verbose', False):
        setlogginglevel('debug')
    logger.debug("Arguments: {args}".format(args=args))
    if args.get('<showname>', False):
        showname = getshowname(" ".join(args['<showname>']))
        logger.info("Showname: '{name}'".format(name=showname))

    if args.get('--watch-next', False):
        watchnext(showname)
    elif args.get('--watch', False):
        watch(showname, args['--watch'])
    elif args.get('--next-episode', False):
        nextepisode(showname)
    elif args.get('--mark-watched', False):
        markwatched(showname, args['--mark-watched'], watched=True,
                    markprevious=args.get('--mark-previous', False))
    elif args.get('--mark-unwatched', False):
        markwatched(showname, args['--mark-unwatched'], watched=False,
                    markprevious=args.get('--mark-previous', False))
    elif args.get('--download', False):
        download(showname)
    elif args.get('--update', False):
        update(showname)
    elif args.get('--rename', False) and args.get('<filename>', False):
        rename(args['<filename>'])
    else:
        print('Unimplemented/unknown arguments "{}".'.format(args))


def watchnext(showname):
    episode = getnextepisode(showname)
    if episode is None:
        print("Couldn't find any new episodes!")
        if yesno("Would you like to update the cache?"):
            update(showname)
            watchnext(showname)  # this could be an endless loop.
        return
    if watchepisode(episode):
        markwatched(episode)


def watch(showname, episodestring):
    seasonnum, episodenum = getepisodeinfo(episodestring)
    assert(seasonnum is not None and episodenum is not None)
    episode = getepisode(showname, seasonnum, episodenum)
    if watchepisode(episode):
        markwatched(episode)


def nextepisode(showname):
    logger.info("nextepisode")
    episode = getnextepisode(showname)
    if episode is None:
        print "No episode found!"
        return
    print("Next episode is: {episode}: {date}".format(episode=episode.getprettyname(),
                                                      date=episode.getairdatestr()).encode('utf8'))


def markwatched(showname, episodestring, markprevious, watched):
    logger.info("markwatched")
    seasonnum, episodenum = getepisodeinfo(episodestring)
    episode = getepisode(showname, seasonnum, episodenum)
    markwatched(episode, markprevious=markprevious, watched=watched)


def download(showname):
    logger.info("download")
    seasonnum, episodenum = getepisodeinfo(args['--download'])
    episode = getepisode(showname, seasonnum, episodenum)
    downloadepisode(episode)


def rename(filenames):
    logger.info("rename")
    # user didn't give an argument. he wants to run it on all files in folder.
    if filenames == []:
        filenames = listdir('.')
    for filename in filenames:
        renameepisode(filename)


def update(showname):
    logger.info("update")
    print("Updating {name}..".format(name=showname))
    getshow(showname, update=True)


if __name__ == '__main__':
    args = docopt(__doc__, version='Series everything v 0.1')
    try:
        main(args)
    except (KeyboardInterrupt, SystemExit):
        print("\nProgram stopped...")
