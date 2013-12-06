import requests
import lxml.html
from datetime import datetime

from tvshowhelper.classes.link import Link
# from tvshowhelper.informationscrapers import random_useragent
from interface import LinkScraperInterface
from tvshowhelper import logger
from tvshowhelper.parallel import parallel_map


class Filestube(LinkScraperInterface):
    _BASE_URL = "http://www.filestube.com/"
    _LIST_URL = (_BASE_URL + "query.html?q={query}&select=All&hosting=24,81&"
                 "page={{pageid}}&sizefrom={sizefrom}&sizeto={sizeto}")
    _LINKS_PER_PAGE = 10
    _NUM_PAGES_SCRAPED = 2

    def getlinks(self, query, numlinks=5, size=(100, 1500)):
        start = datetime.now()
        query = query.replace(" ", "+")
        url = self._LIST_URL.format(query=query, sizefrom=size[0], sizeto=size[1])
        urls = [url.format(pageid=i) for i in range(1, self._NUM_PAGES_SCRAPED + 1)]
        links = parallel_map(self._scrapepage, urls)
        res = []
        for link in links:
            res += link
        links = filter(lambda x: x is not None, res)
        stop = datetime.now()
        logger.debug("getlinks took: {time}".format(time=stop - start))
        return links[:numlinks]

    def _getresponse(self, url):
        try:
            response = requests.get(url)
        except Exception:
            return None
        return response

    def _scrapepage(self, url):
        logger.debug("_scrapepage")
        response = self._getresponse(url)
        if not response:
            print("ERROR: Couldn't connect to filestube!")
            return []
        html = response.text
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
        logger.debug("Number of links: {numlinks}".format(numlinks=len(links)))
        return parallel_map(self._getfilehostlinks, links)

    def _getfilehostlinks(self, url):
        logger.debug("_getfilehostlinks")
        response = self._getresponse(url)
        if not response:
            return None
        html = response.text
        logger.debug("Getting filehost links")
        doc = lxml.html.fromstring(html)
        links = doc.cssselect("pre#copy_paste_links")[0].text_content().strip("\"").strip().split()
        title = doc.cssselect("div.dotter h1")[0].text_content()[:-9]  # -9 here to remove " download"
        # logger.debug("Links: {links}".format(links=links))
        uris = parallel_map(self._validate, links)
        if None in uris:
            return None
        return Link(title=title, uris=uris)

    def _validate(self, link):
        response = self._getresponse(link)
        if not response:
            return None
        logger.debug("Validating link: {link}. Status code: {status}".format(link=link, status=response.status_code))
        if response.status_code != 200 or response.url[-3:] == "404":
            return None
        return link
