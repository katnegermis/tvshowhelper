import os
import subprocess
from datetime import datetime

from settings import VIDEO_COMMAND, SERIES_ROOT_FOLDER, AIR_DATE_FORMAT
import askuser
from seriesfilename import getepisodeinfo


def watch(showname, seasonnum, episodenum, cache=None):
    episode = cache.getepisode(showname, seasonnum, episodenum)
    if episode is not None and episode.airdate > datetime.now():
        print "{} S{}E{} hasn't aired yet! It will air {}".format(showname,
                                                                  seasonnum,
                                                                  episodenum,
                                                                  datetime.strftime(episode.airdate, AIR_DATE_FORMAT))
        return

    showpath = os.path.join(SERIES_ROOT_FOLDER, showname)
    if not os.path.exists(showpath):
        return
    episodepath = None
    for filename in os.listdir(showpath):
        seasonnumtmp, episodenumtmp = getepisodeinfo(filename)
        if seasonnumtmp is None or episodenumtmp is None:
            continue
        if (seasonnum == seasonnumtmp and episodenum == episodenumtmp):
            episodepath = os.path.join(showpath, filename)
            break
    if episodepath is None:
        question = "{} S{}E{} - {} wasn't found. Should we try to download it?".format(showname, seasonnum, episodenum, episode.name)
        if askuser.yesno(question):
            downloadshow(showname, seasonnum, episodenum)
        return
    else:
        print "NOW WATCHING {}".format(episodepath)
        subprocess.call([VIDEO_COMMAND, episodepath.replace(" ", "\ ")],
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


# def markwatched(showname, seasonnum, episodenum, markprevious=False, watched=True, cache=None):
#     if cache is None:
#         cache = SeriesCache()
#     cache = SeriesCache()
#     regex = findshow(showname)
#     showname = regex.showname
#     show = cache.getshow(showname)
#     if markprevious:
#         _markpreviouswatched(show, seasonnum, episodenum, watched=watched)
#     else:
#         _markwatched(show, seasonnum, episodenum, watched=watched)
#     cache.saveshow(show)


# def _markpreviouswatched(show, seasonnum, episodenum, watched=True):
#     for season in show.seasons:
#         if int(season.number) < int(seasonnum):
#             for episode in season.episodes:
#                     episode.watched = watched
#         elif int(season.number) == int(seasonnum):
#             for episode in season.episodes:
#                 if int(episode.number) <= int(episodenum):
#                     episode.watched = watched


# def _markwatched(show, seasonnum, episodenum, watched=True):
#     season = show.getseason(seasonnum)
#     if season is not None:
#         episode = season.getepisode(episodenum)
#         if episode is not None:
#             episode.watched = watched
