from os import path, mkdir
import shutil

from settings import SERIES_ROOT_FOLDER, IF_NOT_SHOW_EXISTS_CREATE_FOLDER
from seriesnamehandler import getepisodeinfo, getshowname


def renameepisode(filename, cache):
    """ Rename a file by guessing what series and episode it is,
    from its' current file name
    """
    print "Analyzing {}".format(filename)
    seasonnumber, episodenumber = getepisodeinfo(filename)
    if None in (seasonnumber, episodenumber):
        print "Couldn't find episode information!".format(filename)
        return False
    showname = getshowname(filename)
    if showname is None:
        print "Didn't match any series"
        return False
    print "Found to be part of {}".format(showname)
    episode = cache.getepisode(showname, seasonnumber, episodenumber)
    if episode is None:
        print "Couldn't find any information on {} S{}E{}".format(showname, seasonnumber, episodenumber)
        return
    __, ext = path.splitext(filename)
    newfilename = episode.getprettyname() + ext
    newfilename = newfilename.replace("/", "-").replace("'", "")
    print "Moving to {}".format(newfilename.encode('utf8'))
    _movefile(filename, newfilename, showname)
    print ""


def _movefile(filename, newfilename, showname):
    if not path.exists(filename):
        print "{} doesn't exist. Would have moved to {}".format(filename, newfilename)
        return
    showfolder = path.join(SERIES_ROOT_FOLDER, showname)
    if not path.exists(showfolder):
        if IF_NOT_SHOW_EXISTS_CREATE_FOLDER:
            mkdir(showfolder)
        else:
            print "{} doesn't exist, and IF_NOT_SHOW_EXISTS_CREATE_FOLDER is set to false. Skipping file!"
    newfilepath = path.join(showfolder, newfilename)
    if path.exists(newfilepath):
        print "{} already exists! Skipping".format(newfilepath)
    shutil.move(filename, newfilepath)
