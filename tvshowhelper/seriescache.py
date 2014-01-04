import sqlite3 as sqlite
from datetime import datetime

from settings import DB_FILE
from tvshowhelper.informationscrapers import imdb
from tvshowhelper.classes.show import Show
from tvshowhelper.classes.season import Season
from tvshowhelper.classes.episode import Episode


SQL_DATE_FORMAT = "%Y-%m-%d"


def _getdbcon():
    db = sqlite.connect(DB_FILE)
    c = db.cursor()
    showstable = """
        CREATE TABLE IF NOT EXISTS shows (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT
        );
        """
    c.execute(showstable)

    episodestable = """
        CREATE TABLE IF NOT EXISTS episodes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            show_id INTEGER,
            number INTEGER,
            name TEXT,
            airdate TEXT,
            description TEXT,
            watched INTEGER,
            season_number INTEGER,
            FOREIGN KEY(show_id) REFERENCES shows(id)
        );
         """
    c.execute(episodestable)
    db.commit()
    return db


def getepisode(showname, seasonnum, episodenum, update=False):
    if not showexists(showname):
        show = imdb.getshow(showname)
        _storeshow(show)
    if update:
        updateshow(showname)
    sql = """
        SELECT e.number, e.name, e.airdate, e.description, e.watched, e.season_number
        FROM shows AS s, episodes AS e
        WHERE s.name = ?
          AND e.season_number = ?
          AND e.number = ?;
        """
    db = _getdbcon()
    c = db.cursor()
    c.execute(sql, (showname, seasonnum, episodenum))
    rows = c.fetchall()
    if rows == []:
        # Episode not found.
        return None
    assert len(rows) == 1, "Duplicate episode in database"
    db.close()
    return _rowtoepisode(showname, rows[0])


def getnextepisode(showname):
    db = _getdbcon()
    db.close()


def markwatched(showname, episode, markprevious=False, watched=True):
    db = _getdbcon()
    db.close()


def updateshow(showname):
    db = _getdbcon()
    # imdb
    db.close()


def showexists(showname):
    db = _getdbcon()
    c = db.cursor()
    sql = """
        SELECT *
        FROM shows
        WHERE name = ?;
        """
    c.execute(sql, (showname,))
    rows = c.fetchall()
    res = len(rows) if rows != [] else 0
    assert res in (0, 1), "Duplicate shows in database!"
    return res == 1


def _rowtoshow(row):
    pass


def _rowtoepisode(showname, row):
    return Episode(number=row[0],
                   name=row[1],
                   airdate=datetime.strptime(row[2], SQL_DATE_FORMAT).date(),
                   description=row[3],
                   watched=row[4],
                   seasonnumber=row[5],
                   showname=showname)


def _storeshow(show):
    sql = """
        INSERT INTO shows (name)
        VALUES (?);
        """
    db = _getdbcon()
    c = db.cursor()
    c.execute(sql, (show.name,))
    db.commit()
    db.close()
    for season in show.seasons:
        _storeepisodes(season.episodes)


def _storeepisodes(episodes):
    showname = episodes[0].showname
    if not showexists(showname):
        show = imdb.getshow(showname)
        _storeshow(show)
    sql = """
        INSERT INTO episodes (number, name, airdate, description, watched, season_number)
        VALUES (?, ?, ?, ?, ?, ?);
        """
    episodetuples = map(lambda e: (e.number, e.name, e.airdate, e.description,
                                   e.watched, e.seasonnumber),
                        episodes)
    db = _getdbcon()
    c = db.cursor()
    c.executemany(sql, episodetuples)
    db.commit()
    db.close()
