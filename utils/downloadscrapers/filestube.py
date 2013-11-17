import requests
import lxml.html

from utils.classes.link import Link
from interface import LinkScraperInterface


class Filestube(LinkScraperInterface):
    _BASE_URL = "http://www.filestube.com/"
    _LIST_URL = (_BASE_URL + "query.html?q={query}&select=All&hosting=24,81&"
                 "page={{pageid}}&sizefrom={sizefrom}&sizeto={sizeto}")
    _LINKS_PER_PAGE = 10

    def getlinks(self, query, numlinks=5, size=(100, 1500)):
        query = query.replace(" ", "+")
        url = self._LIST_URL.format(query=query, sizefrom=size[0], sizeto=size[1])
        pageids = xrange(1, ((numlinks // self._LINKS_PER_PAGE) + 1) + 1)
        downloadpages = []
        for i in pageids:
            downloadpages += self._getdownloadpagelinks(url.format(pageid=i))
        return map(self._getfilehostlinks, downloadpages[:numlinks])

    def _getdownloadpagelinks(self, url):
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
                a_tag = result.cssselect("a.resultsLink")[0]
                link = self._BASE_URL + a_tag.get('href')
                links.append(link)
            except IndexError:
                print "there was no link on the page"
                continue
        return links

    def _getfilehostlinks(self, url):
        html = requests.get(url).text
        doc = lxml.html.fromstring(html)
        links = doc.cssselect("pre#copy_paste_links")[0].text_content().strip("\"").strip().split()
        title = doc.cssselect("div.dotter h1")[0].text_content()[:-9]  # -9 here to remove " download"
        return Link(title=title, uris=links)

if __name__ == '__main__':
    filestube = Filestube()
    print filestube.getlinks("how i met your mother s06e03")
