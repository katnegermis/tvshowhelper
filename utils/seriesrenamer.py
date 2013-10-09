#!/usr/bin/python

import sys
import os
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(ROOT_DIR)
import os
import shutil

import settings as conf
from seriescache import SeriesCache


def rename(filenames):
    cache = SeriesCache()
    for filename in filenames:
        print "Analyzing {}".format(filename)
        seasonnumber, episodenumber = getepisodeinfo(filename)
        if seasonnumber is None or episodenumber is None:
            print "Couldn't find episode information!".format(filename)
        else:
            showregex = findshow(filename)
            if showregex is None:
                print "Didn't match any series"
                continue
            showname = showregex.getshowname()
            print "Found to be part of {}".format(showname)
            episode = cache.getepisode(showname, seasonnumber, episodenumber)
            if episode is None:
                print "Couldn't find any information on {} S{}E{}".format(showname, seasonnumber, episodenumber)
                continue
            fileext = os.path.splitext(filename)[1]
            newfilename = episode.getprettyname(showname=showname, seasonnumber=seasonnumber) + fileext
            newfilename = newfilename.replace("/", "-").replace("'", "")
            print "Moving to {}".format(newfilename.encode('utf8'))
            _movefile(filename, newfilename, showname)
        print ""


def _movefile(filename, newfilename, showname):
    if not os.path.exists(filename):
        print "{} doesn't exist. Would have moved to {}".format(filename, newfilename)
        return
    showfolder = os.path.join(conf.SERIES_ROOT_FOLDER, showname)
    if not os.path.exists(showfolder):
        if conf.IF_NOT_SHOW_EXISTS_CREATE_FOLDER:
            os.mkdir(showfolder)
        else:
            print "{} doesn't exist, and IF_NOT_SHOW_EXISTS_CREATE_FOLDER is set to false. Skipping file!"
    newfilepath = os.path.join(showfolder, newfilename)
    if os.path.exists(newfilepath):
        print "{} already exists! Skipping".format(newfilepath)
    shutil.move(filename, newfilepath)
