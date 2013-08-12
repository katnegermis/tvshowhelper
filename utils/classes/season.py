class Season(object):

    def __init__(self, number, name=None):
        self._number = self._formatnumber(number)
        self._name = name
        self._episodes = []

    def __unicode__(self):
        return unicode(self.getprettyname())

    def __repr__(self):
        return self.getprettyname().encode('utf8')

    def getprettyname(self):
        name = self._name
        if self._name is None or self._name == "":
            name = "Season {}".format(self._number)
        return name

    def getname(self):
        return self._name

    def getnumber(self):
        return self._number

    def getepisodes(self):
        return self._episodes

    def getepisode(self, number):
        number = self._formatnumber(number)
        for episode in self._episodes:
            if episode.getnumber() == number:
                return episode
        return None

    def hasepisode(self, number):
        return self.getepisode(number) is not None

    def addepisode(self, episode):
        # check that episode is an instance of Episode
        self._episodes.append(episode)

    def _formatnumber(self, number):
        return str(number).zfill(2)
