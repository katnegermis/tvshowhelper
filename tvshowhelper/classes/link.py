class Link(object):

    def __init__(self, title, uris):
        self.title = title
        if not isinstance(uris, list):
            uris = [uris]
        self.uris = uris

    def __repr__(self):
        return "{title} ({link})".format(title=self.title, link=self.uris)
