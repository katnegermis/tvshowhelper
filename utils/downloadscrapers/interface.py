from abc import ABCMeta, abstractmethod


class LinkScraperInterface(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def getlinks(self, query):
        pass
