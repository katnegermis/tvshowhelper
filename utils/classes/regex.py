import re


class Regex(object):
    _regex = None
    _name = None

    def __init__(self, regex, name):
        self._name = name
        self._regex = re.compile(regex, re.IGNORECASE)

    def getregex(self):
        return self._regex

    def getshowname(self):
        return self._name
