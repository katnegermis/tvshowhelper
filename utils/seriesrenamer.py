import os
import shutil

from settings.settings import SERIES_ROOT_FOLDER, IF_NOT_SHOW_EXISTS_CREATE_FOLDER
from seriesnamehandler import getepisodeinfo, getshowname


def renameepisode(filenames, cache):
    for filename in filenames:
        print "Analyzing {}".format(filename)
        seasonnumber, episodenumber = getepisodeinfo(filename)
        if None in (seasonnumber, episodenumber):
            print "Couldn't find episode information!".format(filename)
            continue
        else:
            showname = getshowname(filename)
            if showname is None:
                print "Didn't match any series"
                continue
            print "Found to be part of {}".format(showname)
            episode = cache.getepisode(showname, seasonnumber, episodenumber)
            if episode is None:
                print "Couldn't find any information on {} S{}E{}".format(showname, seasonnumber, episodenumber)
                continue
            fileext = os.path.splitext(filename)[1]
            newfilename = episode.getprettyname() + fileext
            newfilename = newfilename.replace("/", "-").replace("'", "")
            print "Moving to {}".format(newfilename.encode('utf8'))
            _movefile(filename, newfilename, showname)
        print ""


def _movefile(filename, newfilename, showname):
    if not os.path.exists(filename):
        print "{} doesn't exist. Would have moved to {}".format(filename, newfilename)
        return
    showfolder = os.path.join(SERIES_ROOT_FOLDER, showname)
    if not os.path.exists(showfolder):
        if IF_NOT_SHOW_EXISTS_CREATE_FOLDER:
            os.mkdir(showfolder)
        else:
            print "{} doesn't exist, and IF_NOT_SHOW_EXISTS_CREATE_FOLDER is set to false. Skipping file!"
    newfilepath = os.path.join(showfolder, newfilename)
    if os.path.exists(newfilepath):
        print "{} already exists! Skipping".format(newfilepath)
    shutil.move(filename, newfilepath)
