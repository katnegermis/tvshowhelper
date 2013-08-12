#!/usr/bin/python

import sys
sys.path.append("/media/storage/Dropbox/Koding/python/series_everything")

import requests
import lxml.html

from utils.classes.link import Link

BASE_URL = "http://www.filestube.com/"
LIST_URL = BASE_URL + "query.html?q={}&select=All&hosting=24,81&page={}&sizefrom={}&sizeto={}"
LINKS_PER_PAGE = 10


def getlinks(query, numlinks=5, size=(100, 1500)):
    # print "Searching for \"{}\" on filestube".format(query)
    query = query.replace(" ", "+")
    linkpages = []
    for i in range(1, (numlinks / LINKS_PER_PAGE + 1) + 1):  # important that integer division is used here.
        url = LIST_URL.format(query, i, size[0], size[1])
        linkpages += querygetlinkpages(url)
    links = []
    for linkpage in linkpages[:numlinks]:
        links.append(linkpagegetlink(linkpage))
    return links


def querygetlinkpages(url):
    try:
        html = requests.get(url).text
    except requests.exceptions.ConnectionError:
        print "ERROR: Couldn't connect to filestube!"
        return []
    doc = lxml.html.fromstring(html)
    results = doc.cssselect("div#newresult")
    links = []
    for result in results:
        try:
            link = BASE_URL + result.cssselect("a.resultsLink")[0].get('href')
            title = result.cssselect("a.resultsLink")[0].get('title')
            links.append(Link(title=title, links=[link]))
        except IndexError:
            # there was no link on the page.
            # this happens if the file is known to be removed from the filehost
            continue
    return links


def linkpagegetlink(link):
    html = requests.get(link.getlinks()[0]).text
    doc = lxml.html.fromstring(html)
    links = doc.cssselect("pre#copy_paste_links")[0].text_content().strip("\"").strip().split()
    return Link(title=link.gettitle(), links=links)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        print getlinks(" ".join(sys.argv[1:]))
    else:
        print getlinks("parks and recreation s05e16")
