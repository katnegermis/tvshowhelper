import requests


JDOWNLOADER_BASE_URL = "http://localhost:10025/"


def download(link, start=True):
    if start:
        url = JDOWNLOADER_BASE_URL + "/action/add/links/grabber0/start1/{}".format(" ".join(link.getlinks()))
    else:
        url = JDOWNLOADER_BASE_URL + "/action/add/links/grabber1/start0/{}".format(" ".join(link.getlinks()))
    requests.get(url)
