import re
import os

from regexes import SERIES_REGEXES

ROOT_DIR = os.path.dirname(os.path.realpath(__file__))

IF_NOT_SHOW_EXISTS_CREATE_FOLDER = True

VIDEO_COMMAND = "vlc"

SERIES_ROOT_FOLDER = "/home/katnegermis/downloads"

CACHE_FILE = os.path.join(ROOT_DIR, "data", "cache.json")

SEASON_EPISODE_REGEX = re.compile("(s|se|season)(?P<season>\d{1,2})(e|ep|episode)(?P<episode>\d{1,2})", re.IGNORECASE)
SEASON_EPISODE_REGEX_EXTRAS = (
    re.compile("((?P<season>\d{1,2})(?P<episode>\d{1,2}))(?!(p|mb))", re.IGNORECASE),
    re.compile("((?P<season>\d{1})(?P<episode>\d{1,2}))(?!(p|mb))", re.IGNORECASE),
)

DOWNLOADERS = (
    {'scraper': 'filestube',
     'downloader': 'jdownloader'},
)

AIR_DATE_FORMAT = "%b. %d, %Y"
