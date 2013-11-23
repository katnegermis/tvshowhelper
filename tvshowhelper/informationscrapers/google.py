import requests
import lxml.html


from tvshowhelper.informationscrapers import random_useragent


def _gethtml(query):
    query = query.replace(' ', '+')
    response = requests.get('https://www.google.com/search?ie=utf-8&q={}'.format(query),
                            headers={'User-Agent': random_useragent()})
    return response.text


def query(query_):
    if not isinstance(query_, str):
        raise TypeError("You can only use strings for queries")
    html = _gethtml(query_)
    links = lxml.html.fromstring(html).cssselect('h3.r a')
    if not links:
        return ()
    return tuple({'link': link.get('href'), 'title': link.text_content()}
                 for link in links)
