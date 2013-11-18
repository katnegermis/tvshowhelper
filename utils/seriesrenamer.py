from os import path, mkdir
import shutil

from settings import SERIES_ROOT_FOLDER, IF_NOT_SHOW_EXISTS_CREATE_FOLDER
from utils.seriesnamehandler import getepisodeinfo, getshowname
from utils import logger


def renameepisode(filename, cache):
    """ Rename a file by guessing what series and episode it is,
    from its' current file name
    """
    logger.info("Analyzing {}".format(filename))
    seasonnumber, episodenumber = getepisodeinfo(filename)
    if None in (seasonnumber, episodenumber):
        logger.warning("Couldn't find episode information!".format(filename))
        return False
    showname = getshowname(filename)
    if showname is None:
        logger.warning("Didn't match any series")
        return False
    logger.info("Found to be part of {}".format(showname))
    episode = cache.getepisode(showname, seasonnumber, episodenumber)
    if episode is None:
        logger.warning("Couldn't find any information on {} S{}E{}".format(showname, seasonnumber, episodenumber))
        return
    __, ext = path.splitext(filename)
    newfilename = episode.getprettyname() + ext
    newfilename = newfilename.replace("/", "-").replace("'", "")
    logger.info("Moving to {}".format(newfilename.encode('utf8')))
    _movefile(filename, newfilename, showname)


def _movefile(filename, newfilename, showname):
    if not path.exists(filename):
        logger.warning("{} doesn't exist. Would have moved to {}".format(filename, newfilename))
        return
    showfolder = path.join(SERIES_ROOT_FOLDER, showname)
    if not path.exists(showfolder):
        if IF_NOT_SHOW_EXISTS_CREATE_FOLDER:
            mkdir(showfolder)
        else:
            logger.warning("{} doesn't exist, and IF_NOT_SHOW_EXISTS_CREATE_FOLDER "
                            "is set to false. Skipping file!")
    newfilepath = path.join(showfolder, newfilename)
    if path.exists(newfilepath):
        logger.info("{} already exists! Skipping".format(newfilepath))
    shutil.move(filename, newfilepath)
