import json
import codecs
import shutil
from datetime import datetime

# import settings as conf
from settings import AIR_DATE_FORMAT, CACHE_FILE
from utils.informationscrapers import imdb
from utils.classes.show import Show
from utils.classes.season import Season
from utils.classes.episode import Episode


def log(text):
    pass


class SeriesCache(object):
    """ A dictionary of shows, with show names as keys.
    Each show is either serialized (an instance of Show) or not (a dictionary).
    Each show will be serialized before returned from this class.
    """
    _shows = None

    def getshow(self, showname, update=False):
        """ Retrieve a show from the cache. If it does not already exist in
        the cache, it will be retrieved from the internet. At this point in time
        only imdb is searched.
        """
        # cache hit, not forced update
        if not update and self._shows is not None and showname in self._shows:
            if not isinstance(self._shows[showname], Show):
                self._shows[showname] = self._dicttoshow(showname, self._shows[showname])
            return self._shows[showname]
        # check if we have already read something from cache
        if self._shows is None:
            self._shows = self._readcache()
            # check if cache was empty
            if self._shows is None:
                self._shows = {}
        # check if we should update show cache
        if update or showname not in self._shows:
            showtmp = imdb.getshow(showname)
            if showname in self._shows:
                showtmp = self._saveepisodeproperties(showname, self._shows[showname], showtmp)
            self._shows[showname] = showtmp
            self._savecache(self._shows)
        # make sure that show is instance of Show
        if not isinstance(self._shows[showname], Show):
            self._shows[showname] = self._dicttoshow(showname, self._shows[showname])
        return self._shows[showname]

    def getseason(self, showname, seasonnum, update=False):
        """ Retrieve a season from a show, from the cache.
        """
        show = self.getshow(showname, update=update)
        # make sure that the cache is up to date
        if not show.hasseason(seasonnum) and not update:
            show = self.getshow(showname, update=True)
            if not show.hasseason(seasonnum):
                return None
        return show.getseason(seasonnum)

    def getepisode(self, showname, seasonnum, episodenum, update=False):
        """ Retrieve an episode from a season from a show, from the cache.
        """
        season = self.getseason(showname, seasonnum, update=update)
        # make sure that the cache is up to date
        if (season is None or not season.hasepisode(episodenum)) and not update:
            season = self.getseason(showname, seasonnum, update=True)
            if season is None or not season.hasepisode(episodenum):
                return None
        return season.getepisode(episodenum)

    def saveshow(self, show):
        self._shows[show.name] = show
        self._savecache(self._shows)

    def getnextepisode(self, showname):
        show = self.getshow(showname)
        nextepisode = None
        nextseason = None
        for season in show.seasons:
            for episode in season.episodes:
                if episode.watched:
                    continue
                if nextepisode is None:
                    nextepisode = episode
                if nextseason is None:
                    nextseason = season
                if (int(season.number) < int(nextseason.number) or
                        int(season.number) == int(nextseason.number) and
                        int(episode.number) < int(nextepisode.number)):
                    nextepisode = episode
                    nextseason = season
        return nextseason, nextepisode

    def markwatched(self, showname, seasonnum, episodenum, markprevious=False, watched=True):
        show = self.getshow(showname)
        # mark watched according to arguments
        self.saveshow(show)

    def _saveepisodeproperties(self, showname, oldshow, newshow):
        if not isinstance(oldshow, Show):
            oldshow = self._dicttoshow(showname, oldshow)
        for oldseason in oldshow.seasons:
            if not newshow.hasseason(oldseason.number):
                continue
            newseason = newshow.getseason(oldseason.number)
            for oldepisode in oldseason.episodes:
                if not newseason.hasepisode(oldepisode.number):
                    continue
                newepisode = newseason.getepisode(oldepisode.number)
                newepisode.setproperties(**oldepisode.getproperties())
        return newshow

    def _readcache(self):
        log("reading cache")
        try:
            with codecs.open(CACHE_FILE, 'r', 'utf8') as f:
                return json.loads(f.read())
        except (IOError, ValueError) as e:
            log("{}.\n\"{}\".".format(e, CACHE_FILE))
            return None

    def _savecache(self, shows):
        log("Saving cache")
        try:
            with codecs.open(CACHE_FILE + ".tmp", 'w+', 'utf8') as f:
                f.write(self._serializeshows(shows))
                f.flush()
            shutil.move(CACHE_FILE + ".tmp", CACHE_FILE)
        except IOError:
            log("Couldn't write to cache \"{}\"".format(CACHE_FILE))

    def _serializeshows(self, shows):
        """ Serialize shows to json text """
        log("Serializing data")
        for showname in shows:
            if isinstance(shows[showname], Show):
                shows[showname] = self._showtodict(shows[showname])
        return json.dumps(shows, indent=4)

    def _dicttoshow(self, showname, dic):
        show = Show(name=showname, imdburl=dic['imdburl'])
        for seasonnum in dic['season']:
            season = Season(number=seasonnum, name="{} - {}".format(showname, seasonnum))
            show.addseason(season)
            for episodenum in dic['season'][seasonnum]['episode']:

                episode = Episode(number=episodenum,
                                  name=dic['season'][seasonnum]['episode'][episodenum]['name'],
                                  airdate=datetime.strptime(dic['season'][seasonnum]['episode'][episodenum]['airdate'], AIR_DATE_FORMAT),
                                  description=dic['season'][seasonnum]['episode'][episodenum]['description'],
                                  watched=dic['season'][seasonnum]['episode'][episodenum]['watched'])
                season.addepisode(episode)
        return show

    def _showtodict(self, show):
        """ Convert show to a dictionary """
        obj = {'season': {}}
        obj['imdburl'] = show.imdburl
        for season in show.seasons:
            obj['season'][season.number] = {'episode': {}}
            for episode in season.episodes:
                obj['season'][season.number]['episode'][episode.number] = {
                    'name': episode.name,
                    'watched': episode.watched,
                    'description': episode.description,
                    'airdate': datetime.strftime(episode.airdate, AIR_DATE_FORMAT),
                }
        return obj
