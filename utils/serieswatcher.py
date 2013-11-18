import subprocess

from settings import VIDEO_COMMAND
from seriesnamehandler import getepisodepath
from seriesdownloader import downloadepisode
from utils import askuser
from utils import logger


def watchepisode(episode):
    """ Watch episode.
    Will return True if the show was seen, False otherwise.
    """
    assert(episode is not None)
    if not episode.aired:
        logger.info("{} S{}E{} hasn't aired yet! It will air {}.".format(episode.getprettyname(), episode.getairdatestr()))
        return False
    episodepath = getepisodepath(episode.showname, episode)
    if episodepath is None:
        _doesntexist_shoulddownload(episode)
        return False  # do something here, based on response from doesntexist_shoulddownload

    logger.info("Now watching {} ({})".format(episode.getprettyname(), episodepath))
    subprocess.call([VIDEO_COMMAND, episodepath],
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # After episode has been watched, tell user of airdate/episode name of next episode
    if not askuser.yesno("Should '{}' be marked as watched?".format(episode.getprettyname())):
        return False
    return True


def _doesntexist_shoulddownload(episode):
    question = "{name} ({airdate}) wasn't found. Would you try to download it?".format(name=episode.getprettyname(),
                                                                                       airdate=episode.getairdatestr())
    if askuser.yesno(question):
        downloadepisode(episode)
