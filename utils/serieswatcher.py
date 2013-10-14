import subprocess
from datetime import datetime

from settings.settings import VIDEO_COMMAND, AIR_DATE_FORMAT
from seriesnamehandler import getepisodepath
from seriesdownloader import downloadepisode
from utils import askuser


def watchepisode(episode):
    """ Watch a specific episode from the show showname.
    Will return True if the show was seen, False otherwise.
    """
    if episode is not None and episode.airdate > datetime.now():
        print "{} S{}E{} hasn't aired yet! It will air {}.".format(episode.showname, episode.seasonnumber, episode.number,
                                                                   datetime.strftime(episode.airdate, AIR_DATE_FORMAT))
        return False
    episodepath = getepisodepath(episode.showname, episode)
    if episodepath is None:
        _doesntexist_shoulddownload(episode)
        return False  # do something here, based on response from doesntexist_shoulddownload

    print "NOW WATCHING {}".format(episodepath)
    subprocess.call([VIDEO_COMMAND, episodepath],
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if not askuser.yesno("Should '{}' be marked as watched?".format(episode.getprettyname())):
        return False
    return True


def _doesntexist_shoulddownload(episode):
    question = "The {} S{}E{} wasn't found. Would you try to download it?".format(episode.showname, episode.seasonnumber, episode.number)
    if askuser.yesno(question):
        downloadepisode(episode)
