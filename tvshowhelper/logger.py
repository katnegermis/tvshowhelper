import logging

logger = logging.getLogger('series_everything')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


def setlevel(level):
    if level == 'debug':
        l = logging.DEBUG
    else:
        l = logging.INFO
    ch.setLevel(l)
