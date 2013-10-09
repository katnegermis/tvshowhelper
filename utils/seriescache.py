import sys
sys.path.append("..")
import json
import codecs
import shutil

import settings as conf
from utils.informationscrapers import imdb
from utils.classes.show import Show
from utils.classes.season import Season
from utils.classes.episode import Episode


def log(text):
    pass


class SeriesCache:
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

    def getseason(self, showname, seasonnumber, update=False):
        """ Retrieve a season from a show, from the cache.
        """
        show = self.getshow(showname, update=update)
        # make sure that the cache is up to date
        if not show.hasseason(seasonnumber) and not update:
            show = self.getshow(showname, update=True)
            if not show.hasseason(seasonnumber):
                return None
        return show.getseason(seasonnumber)

    def getepisode(self, showname, seasonnumber, episodenumber, update=False):
        """ Retrieve an episode from a season from a show, from the cache.
        """
        season = self.getseason(showname, seasonnumber, update=update)
        # make sure that the cache is up to date
        if (season is None or not season.hasepisode(episodenumber)) and not update:
            season = self.getseason(showname, seasonnumber, update=True)
            if season is None or not season.hasepisode(episodenumber):
                return None
        return season.getepisode(episodenumber)

    def saveshow(self, show):
        self._shows[show.name] = show
        self._savecache(self._shows)

    def _saveepisodeproperties(self, showname, oldshow, newshow):
        if not isinstance(oldshow, Show):
            oldshow = self._dicttoshow(showname, oldshow)
        for oldseason in oldshow.seasons:
            if not newshow.hasseason(oldseason.getnumber()):
                continue
            newseason = newshow.getseason(oldseason.getnumber())
            for oldepisode in oldseason.getepisodes():
                if not newseason.hasepisode(oldepisode.number):
                    continue
                newepisode = newseason.getepisode(oldepisode.number)
                newepisode.setproperties(**oldepisode.getproperties())
        return newshow

    def _readcache(self):
        log("reading cache")
        try:
            with codecs.open(conf.CACHE_FILE, 'r', 'utf8') as f:
                return json.loads(f.read())
        except (IOError, ValueError) as e:
            log("{}.\n\"{}\".".format(e, conf.CACHE_FILE))
            return None

    def _savecache(self, shows):
        log("Saving cache")
        try:
            with codecs.open(conf.CACHE_FILE + ".tmp", 'w+', 'utf8') as f:
                f.write(self._serializeshows(shows))
                f.flush()
            shutil.move(conf.CACHE_FILE + ".tmp", conf.CACHE_FILE)
        except IOError:
            log("Couldn't write to cache \"{}\"".format(conf.CACHE_FILE))

    def _serializeshows(self, shows):
        """ Serialize shows to json text """
        log("Serializing data")
        for showname in shows:
            if isinstance(shows[showname], Show):
                shows[showname] = self._showtodict(shows[showname])
        return json.dumps(shows, indent=4)

    def _dicttoshow(self, showname, dictionary):
        show = Show(name=showname, imdburl=dictionary['imdburl'])
        for seasonnumber in dictionary['season']:
            season = Season(number=seasonnumber, name="{} - {}".format(showname, seasonnumber))
            show.addseason(season)
            for episodenumber in dictionary['season'][seasonnumber]['episode']:
                episode = Episode(number=episodenumber,
                                  name=dictionary['season'][seasonnumber]['episode'][episodenumber]['name'],
                                  airdate=dictionary['season'][seasonnumber]['episode'][episodenumber]['airdate'],
                                  description=dictionary['season'][seasonnumber]['episode'][episodenumber]['description'],
                                  watched=dictionary['season'][seasonnumber]['episode'][episodenumber]['watched'])
                season.addepisode(episode)
        return show

    def _showtodict(self, show):
        """ Convert show to a dictionary """
        obj = {'season': {}}
        obj['imdburl'] = show.getimdburl()
        for season in show.seasons:
            obj['season'][season.getnumber()] = {'episode': {}}
            for episode in season.getepisodes():
                obj['season'][season.getnumber()]['episode'][episode.number] = {
                    'name': episode.name,
                    'watched': episode.watched,
                    'description': episode.description,
                    'airdate': episode.airdate
                }
        return obj
