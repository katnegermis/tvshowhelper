from abc import ABCMeta, abstractmethod


class DownloaderInterface(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def download(self, uri=None, autostart=True):
        pass
