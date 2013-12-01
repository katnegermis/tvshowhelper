import requests
import lxml.html
from datetime import datetime

from tvshowhelper.classes.link import Link
from interface import LinkScraperInterface
from tvshowhelper import logger
from tvshowhelper.parallel import parallel_map


class Filestube(LinkScraperInterface):
    _BASE_URL = "http://www.filestube.com/"
    _LIST_URL = (_BASE_URL + "query.html?q={query}&select=All&hosting=24,81&"
                 "page={{pageid}}&sizefrom={sizefrom}&sizeto={sizeto}")
    _LINKS_PER_PAGE = 10

    def getlinks(self, query, numlinks=5, size=(100, 1500)):
        start = datetime.now()
        query = query.replace(" ", "+")
        url = self._LIST_URL.format(query=query, sizefrom=size[0], sizeto=size[1])
        links = []
        for i in range(5):
            downloadpages = self._getdownloadpagelinks(url.format(pageid=i))
            tmp_links = parallel_map(self._getfilehostlinks, downloadpages)
            links = filter(lambda x: x is not None, parallel_map(self.validate, tmp_links))
            if len(links) >= numlinks:
                break
        stop = datetime.now()
        logger.debug("getlinks took: {time}".format(time=stop - start))
        return links[:numlinks]

    def validate(self, link):
        for uri in link.uris:
            response = requests.get(uri)
            logger.debug("{link}: {response}: {status}".format(link=uri, response=response.url, status=response.status_code))
            if response.status_code != 200 or response.url[-3:] == "404":
                return
        return link

    def _getdownloadpagelinks(self, url):
        try:
            html = requests.get(url).text
        except requests.exceptions.ConnectionError:
            print("ERROR: Couldn't connect to filestube!")
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
                print("there was no link on the page")
                continue
        return links

    def _getfilehostlinks(self, url):
        html = requests.get(url).text
        doc = lxml.html.fromstring(html)
        links = doc.cssselect("pre#copy_paste_links")[0].text_content().strip("\"").strip().split()
        title = doc.cssselect("div.dotter h1")[0].text_content()[:-9]  # -9 here to remove " download"
        return Link(title=title, uris=links)

