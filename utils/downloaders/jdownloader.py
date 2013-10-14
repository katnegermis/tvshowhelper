from time import sleep
from subprocess import Popen, PIPE

import requests

from interface import DownloaderInterface


class Jdownloader(DownloaderInterface):
    _JDOWNLOADER_BASE_URL = "http://localhost:10025/"

    def download(self, link, start=True):
        if not self._running():
            self._start()
        if start:
            url = self._JDOWNLOADER_BASE_URL + "/action/add/links/grabber0/start1/{}".format(" ".join(link.uris))
        else:
            url = self._JDOWNLOADER_BASE_URL + "/action/add/links/grabber1/start0/{}".format(" ".join(link.uris))
        requests.get(url)

    def _running(self):
        return False

    def _start(self):
        print "Starting JDownloader..."
        Popen(['jdownloader'], stdout=PIPE, stderr=PIPE, stdin=PIPE)
        sleep(10)
