class Link(object):

    def __init__(self, title, links):
        self._title = title
        self._links = links

    def gettitle(self):
        return self._title

    def getlinks(self):
        return self._links
