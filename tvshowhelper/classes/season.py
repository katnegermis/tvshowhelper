class Season(object):

    def __init__(self, number, name=None):
        self.number = self._formatnumber(number)
        self.name = name
        self.episodes = []

    def __unicode__(self):
        return unicode(self.getprettyname())

    def __repr__(self):
        return self.getprettyname()

    def getprettyname(self):
        name = self.name
        if name is None or name == "":
            name = "Season {}".format(self.number)
        return name

    def getepisode(self, number):
        number = self._formatnumber(number)
        for episode in self.episodes:
            if episode.number == number:
                return episode
        return None

    def hasepisode(self, number):
        return self.getepisode(number) is not None

    def addepisode(self, episode):
        # check that episode is an instance of Episode
        self.episodes.append(episode)

    def _formatnumber(self, number):
        return str(number).zfill(2)
