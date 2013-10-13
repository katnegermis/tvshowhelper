class Link(object):

    def __init__(self, title, uris):
        self.title = title
        if not isinstance(uris, list):
            uris = [uris]
        self.uris = uris
