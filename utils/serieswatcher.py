import subprocess
from datetime import datetime

from settings import VIDEO_COMMAND, AIR_DATE_FORMAT
from utils.seriesnamehandler import getepisodepath
from utils import askuser


def watch(showname, episode, cache=None):
    """ Watch a specific episode from the show showname.
    Will return True if the show was seen, False otherwise.
    """
    if episode is not None and episode.airdate > datetime.now():
        print "{} S{}E{} hasn't aired yet! It will air {}.".format(showname, episode.seasonnumber, episode.number,
                                                                  datetime.strftime(episode.airdate, AIR_DATE_FORMAT))
        return False

    episodepath = getepisodepath(showname, episode)
    if episodepath is None:
        _doesntexist_shoulddownload(showname, episode)
        return False  # do something here, based on response from doesntexist_shoulddownload

    print "NOW WATCHING {}".format(episodepath)
    subprocess.call([VIDEO_COMMAND, episodepath],
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if not askuser.yesno("Should '{}' be marked as watched?".format(episode.getprettyname(showname))):
        return False
    return True


def _doesntexist_shoulddownload(showname, episode):
    question = "The {} S{}E{} wasn't found. Would you try to download it?".format(showname, episode.seasonnumber, episode.number)
    if askuser.yesno(question):
        downloadshow(showname, episode)
