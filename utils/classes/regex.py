import re


class Regex(object):

    def __init__(self, regex, showname):
        self.showname = showname
        self.regex = re.compile(regex, re.IGNORECASE)
