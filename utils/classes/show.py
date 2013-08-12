class Show(object):

    def __init__(self, name, imdburl=None):
        self._name = name
        self._imdburl = imdburl
        self._seasons = []

    def __unicode__(self):
        return unicode(self._name)

    def __repr__(self):
        return self._name.encode('utf8')

    def addseason(self, season):
        # check that season is an instance of Season
        self._seasons.append(season)

    def getseasons(self):
        return self._seasons

    def getseason(self, number):
        number = self._formatnumber(number)
        for season in self._seasons:
            if number == season.getnumber():
                return season
        return None

    def hasseason(self, number):
        return self.getseason(number) is not None

    def _formatnumber(self, number):
        return str(number).zfill(2)

    def getname(self):
        return self._name

    def getimdburl(self):
        return self._imdburl
