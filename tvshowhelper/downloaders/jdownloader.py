from time import sleep
from subprocess import Popen, PIPE

import requests
import requests.exceptions

from interface import DownloaderInterface
from tvshowhelper import logger


class Jdownloader(DownloaderInterface):
    _JDOWNLOADER_BASE_URL = "http://localhost:10025/"

    def download(self, link, start=True):
        if not self._running():
            self._start()
        if start:
            url = self._JDOWNLOADER_BASE_URL + "/action/add/links/grabber0/start1/{}".format(" ".join(link.uris))
        else:
            url = self._JDOWNLOADER_BASE_URL + "/action/add/links/grabber1/start0/{}".format(" ".join(link.uris))
        try:
            requests.get(url)
        except requests.exceptions.ConnectionError:
            print("JDownloader doesn't seem to be running. Please open it and try again!")
            print("The link is: {l}".format(l=link))

    def _running(self):
        p = Popen(["ps", "-A"], stdout=PIPE)
        out, err = p.communicate()
        for line in out.splitlines():
            if 'jdownloader' in line:
                return True
        return False

    def _start(self):
        print("Starting JDownloader...")
        try:
            Popen(['jdownloader'], stderr=PIPE)
        except Exception, e:
            print "Error while starting JDownloader: {err}".format(err=e)
            return
        while not self._running():
            sleep(2)
        sleep(20)
