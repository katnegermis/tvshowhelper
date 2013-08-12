import requests
import json


def search(search):
    """
    Uses the google api to perform a google search.

    Does not yet catch any exceptions. Bad.
    """

    # both cx and key are personal, and belong to katnegermis
    cx = "014236546466015831762:fwk6wyz_ku8"
    key = "AIzaSyBk9ZmLPYDCqC5etOi1hT-Sir7FKNjrlm4"

    url = ("https://www.googleapis.com/customsearch/v1?"
           "key={0}&alt=json&cx={1}&q={2}".format(key, cx, search))
    return json.loads(requests.get(url).text)


def getimdblink(series):
    try:
        return search("{} series imdb".format(series))['items'][0]['link']
    except KeyError:
        raise Exception("You have probably used up your 100 daily searches!")

if __name__ == '__main__':
    print getimdblink("parks and recreation").encode('utf8')
