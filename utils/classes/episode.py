class Episode(object):

    def __init__(self, number, showname=None, name=None, airdate=None, seasonnumber=None, description=None, watched=False):
        self.number = self._formatnumber(number)
        self.name = name
        self.airdate = airdate
        self.description = description
        self.watched = watched
        self.seasonnumber = seasonnumber
        self.showname = showname

    def __unicode__(self):
        return unicode(self.name)

    def __repr__(self):
        return self.name

    def getprettyname(self):
        name = ""
        if self.name is not None:
            name = u" - {}".format(self.name)
        return u"{} S{}E{}{}".format(self.showname, self.seasonnumber, self.number, name)

    def _formatnumber(self, number):
        return str(number).zfill(2)

    def setproperties(self, **kwargs):
        self.watched = kwargs.get('watched', False)
        self.name = kwargs.get('name', None)
        self.airdate = kwargs.get('airdate', None)
        self.description = kwargs.get('description', None)

    def getproperties(self):
        return {
            'watched': self.watched,
            'name': self.name,
            'airdate': self.airdate,
            'description': self.description,
        }
