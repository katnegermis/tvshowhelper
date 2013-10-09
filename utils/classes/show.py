class Show(object):

    def __init__(self, name, imdburl=None):
        self.name = name
        self.imdburl = imdburl
        self.seasons = []

    def __unicode__(self):
        return unicode(self.name)

    def __repr__(self):
        return self.name.encode('utf8')

    def addseason(self, season):
        # check that season is an instance of Season
        self.seasons.append(season)

    def getseason(self, number):
        number = self._formatnumber(number)
        for season in self.seasons:
            if number == season.getnumber():
                return season
        return None

    def hasseason(self, number):
        return self.getseason(number) is not None

    def _formatnumber(self, number):
        return str(number).zfill(2)
