import re
from datetime import datetime

class Episode(object):

    def __init__(self, number, name=None, airdate=None, description=None, watched=False):
        self._number = self._formatnumber(number)
        self._name = name
        self._airdate =  airdate
        self._description = description
        self._watched = watched

    def __unicode__(self):
        return unicode(self.getname())

    def __repr__(self):
        return self.getname().encode('utf8')

    def getprettyname(self, showname, seasonnumber):
        seasonnumber = str(seasonnumber).zfill(2)
        name = ""
        if self._name is not None:
            name = u" - {}".format(self._name)
        return u"{} S{}E{}{}".format(showname, seasonnumber, str(self._number).zfill(2), name)

    def getname(self):
        return self._name

    def getairdate(self):
        return self._airdate

    def getdescription(self):
        return self._description

    def getnumber(self):
        return self._number

    def getwatched(self):
        return self._watched

    def watched(self):
        return self._watched

    def setwatched(self, watched):
        self._watched = watched

    def _formatnumber(self, number):
        return str(number).zfill(2)

    def setproperties(self, **kwargs):
        self._watched = kwargs.get('watched', False)
        self._name = kwargs.get('name', None)
        self._airdate = kwargs.get('airdate', None)
        self._description = kwargs.get('description', None)

    def getproperties(self):
        return {
            'watched': self._watched,
            'name': self._name,
            'airdate': self._airdate,
            'description': self._description,
        }
