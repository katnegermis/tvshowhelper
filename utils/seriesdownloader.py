from settings import DOWNLOADERS
from utils import askuser
from utils.importer import doimport, modulejoin
from utils import logger

DOWNLOADSCRAPERS_MODULE = modulejoin("utils", "downloadscrapers")
DOWNLOADERS_MODULE = modulejoin("utils", "downloaders")


def downloadepisode(episode, start=True):
    query = "{} S{}E{}".format(episode.showname, episode.seasonnumber, episode.number)
    return _download(query, start=start)


def _download(query, start=False):
    if len(DOWNLOADERS) == 1:
        downloadtype = DOWNLOADERS[0]
    else:
        downloadtype = askuser.multipleoptions("Which downloader would you like to use?", DOWNLOADERS, lambda x: x['downloader'])
    if downloadtype is None:
        return False

    if len(downloadtype['scrapers']) == 1:
        scrapermodule = modulejoin(DOWNLOADSCRAPERS_MODULE, downloadtype['scrapers'][0], downloadtype['scrapers'][0].capitalize())
    else:
        scrapertype = askuser.multipleoptions("Which download scraper would you like to use?", downloadtype['scrapers'])
        scrapermodule = modulejoin(DOWNLOADSCRAPERS_MODULE, scrapertype, scrapertype.capitalize())

    try:
        Scrapercls = doimport(scrapermodule)
    except ImportError:
        logger.critical("Couldn't import scraper '{}' ({})".format(scrapertype, scrapermodule))
    scraper = Scrapercls()
    links = scraper.getlinks(query)
    downloadmodule = modulejoin(DOWNLOADERS_MODULE, downloadtype['downloader'], downloadtype['downloader'].capitalize())
    try:
        Downloader = doimport(downloadmodule)
    except ImportError:
        logger.critical("Couldn't import downloader '{}' ({})".format(downloadtype, downloadmodule))

    downloader = Downloader()

    link = askuser.multipleoptions("Which file should we download?", links, lambda x: x.title)
    if link is None:
        logger.info("No link chosen")
        return False
    downloader.download(link)
    # report progress
    # use seriesrenamer when download complete
    return True
