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
from tvshowhelper.seriesdownloader import downloadepisode
from tvshowhelper.seriesrenamer import renameepisode
from tvshowhelper.askuser import yesno
from tvshowhelper.logger import logger, setlevel as setlogginglevel
from tvshowhelper.seriescache import getepisode, getnextepisode, markwatched


def main(args):
    if args.get('--verbose', False):
        setlogginglevel('debug')
    logger.debug("Arguments: {args}".format(args=args))
    if args.get('<showname>', False):
        showname = getshowname(" ".join(args['<showname>']))
        logger.info("Showname: '{name}'".format(name=showname))

    # Decide what function was requested.
    if args.get('--watch-next', False):
        _watchnext(showname)
    elif args.get('--watch', False):
        _watch(showname, args['--watch'])
    elif args.get('--next-episode', False):
        _nextepisode(showname)
    elif args.get('--mark-watched', False):
        _markwatched(showname, args['--mark-watched'], watched=True,
                     markprevious=args.get('--mark-previous', False))
    elif args.get('--mark-unwatched', False):
        _markwatched(showname, args['--mark-unwatched'], watched=False,
                     markprevious=args.get('--mark-previous', False))
    elif args.get('--download', False):
        _download(showname)
    elif args.get('--update', False):
        _update(showname)
    elif args.get('--rename', False) and args.get('<filename>', False):
        _rename(args['<filename>'])
    else:
        print('Unimplemented/unknown arguments "{}".'.format(args))


def _watchnext(showname):
    episode = getnextepisode(showname)
    if episode is None:
        print("Couldn't find any new episodes!")
        if yesno("Would you like to update the cache?"):
            _update(showname)
            _watchnext(showname)  # this could be an endless loop.
        return
    if watchepisode(episode):
        markwatched(episode)


def _watch(showname, episodestring):
    seasonnum, episodenum = getepisodeinfo(episodestring)
    assert(seasonnum is not None and episodenum is not None)
    episode = getepisode(showname, seasonnum, episodenum)
    if watchepisode(episode):
        markwatched(episode)


def _nextepisode(showname):
    logger.info("_nextepisode")
    episode = getnextepisode(showname)
    if episode is None:
        print "No episode found!"
        return
    print("Next episode is: {episode}: {date}".format(episode=episode.getprettyname(),
                                                      date=episode.getairdatestr()).encode('utf8'))


def _markwatched(showname, episodestring, markprevious, watched):
    logger.info("markwatched")
    seasonnum, episodenum = getepisodeinfo(episodestring)
    episode = getepisode(showname, seasonnum, episodenum)
    markwatched(episode, markprevious=markprevious, watched=watched)


def _download(showname):
    logger.info("download")
    seasonnum, episodenum = getepisodeinfo(args['--download'])
    episode = getepisode(showname, seasonnum, episodenum)
    downloadepisode(episode)


def _rename(filenames):
    logger.info("rename")
    # user didn't give an argument. he wants to run it on all files in folder.
    if filenames == []:
        filenames = listdir('.')
    for filename in filenames:
        renameepisode(filename)


def _update(showname):
    logger.info("update")
    print("Updating {name}..".format(name=showname))
    getshow(showname, update=True)


if __name__ == '__main__':
    args = docopt(__doc__, version='Series everything v 0.1')
    try:
        main(args)
    except (KeyboardInterrupt, SystemExit):
        print("\nProgram stopped...")
