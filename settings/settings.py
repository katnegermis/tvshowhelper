import re
import os

""" Root directory of this program. Don't touch unless you decide to restructure it. """
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

""" Path to file that contains information about user's shows. """
CACHE_FILE = os.path.join(ROOT_DIR, "cache.json")

""" TV-series root folder. """
SERIES_ROOT_FOLDER = "/home/katnegermis/downloads"

""" Folder where series are downloaded to. """
SERIES_DOWNLOAD_FOLDER = "/home/katnegermis/downloads"

""" Should the download folder be searched for episodes to watch? """
SEARCH_DOWNLOAD_FOLDER = True

""" If this is set to true, a folder with the series' name will be created in
SERIES_ROOT_FOLDER, in case it doesn't exist, wherein all files of that series
will be placed."""
IF_NOT_SHOW_EXISTS_CREATE_FOLDER = True

""" Program used to play videos. """
VIDEO_COMMAND = "vlc"

""" Default regex to find season- and episode information in filenames.
If file name matches this regex, no action is required by the user."""
SEASON_EPISODE_REGEX = re.compile("(s|se|season)(?P<season>\d{1,2})(e|ep|episode)(?P<episode>\d{1,2})", re.IGNORECASE)

""" If file name doesn't match SEASON_EPISODE_REGEX, the following regexes will be tried.
The user will be asked to choose from the list of matching regexes. """
SEASON_EPISODE_REGEX_EXTRAS = (
    re.compile("((?P<season>\d{1,2})(?P<episode>\d{1,2}))(?!(p|mb))", re.IGNORECASE),
    re.compile("((?P<season>\d)(?P<episode>\d{1,2}))(?!(p|mb))", re.IGNORECASE),
)

DOWNLOADERS = (
    {'downloader': 'jdownloader',
     'scrapers': ['filestube']},
)

""" ###################################################### """
""" You don't have to worry about anything below this line """
""" ###################################################### """

# Date format used to store dates in the cache.
AIR_DATE_FORMAT = "%b. %d, %Y"
