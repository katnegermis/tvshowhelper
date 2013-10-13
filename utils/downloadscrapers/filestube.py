import requests
import lxml.html

from utils.classes.link import Link
from interface import LinkScraperInterface


class Filestube(LinkScraperInterface):
    _BASE_URL = "http://www.filestube.com/"
    _LIST_URL = _BASE_URL + "query.html?q={}&select=All&hosting=24,81&page={}&sizefrom={}&sizeto={}"
    _LINKS_PER_PAGE = 10

    def getlinks(self, query, numlinks=5, size=(100, 1500)):
        query = query.replace(" ", "+")
        linkpages = []
        for i in range(1, ((numlinks / self._LINKS_PER_PAGE) + 1) + 1):  # important that integer division is used here.
            url = self._LIST_URL.format(query, i, size[0], size[1])
            linkpages += self._querygetlinkpages(url)
        links = []
        for linkpage in linkpages[:numlinks]:
            links.append(self._linkpagegetlink(linkpage))
        return links

    def _querygetlinkpages(self, url):
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
                url = self._BASE_URL + result.cssselect("a.resultsLink")[0].get('href')
                title = result.cssselect("a.resultsLink")[0].get('title')
                links.append(Link(title=title, uris=url))
            except IndexError:
                # there was no link on the page.
                # this happens if the file is known to be removed from the filehost
                continue
        return links

    def _linkpagegetlink(self, link):
        html = requests.get(link.uris[0]).text
        doc = lxml.html.fromstring(html)
        links = doc.cssselect("pre#copy_paste_links")[0].text_content().strip("\"").strip().split()
        return Link(title=link.title, uris=links)
