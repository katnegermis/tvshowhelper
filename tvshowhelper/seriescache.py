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
    """ Get a specific episode from a show. Possibly update the show cache.

    """
    # Check if show exists in database, or try to find it on IMDB.
    if not showexists(showname):
        print("'{show}' not found in database!".format(show=showname))
        show = imdb.getshow(showname)
        if show is None:
            # Show not found on imdb.
            return None
        _storeshow(show)
    if update:
        updateshow(showname)
    # Show exists. Try to find requested episode.
    sql = """
        SELECT e.number, e.name, e.airdate, e.description, e.watched, e.season_number
        FROM shows AS s, episodes AS e
        WHERE s.name = ?
          AND s.id = e.show_id
          AND e.season_number = ?
          AND e.number = ?;
        """
    db = _getdbcon()
    c = db.cursor()
    c.execute(sql, (showname, seasonnum, episodenum))
    rows = c.fetchall()
    if rows == []:
        # Episode wasn't found.
        print("{show} S{s}E{e} not found in database!".format(show=showname,
                                                              s=seasonnum,
                                                              e=episodenum))
        return None
    # Episode found.
    assert len(rows) == 1, "Duplicate episode in database"
    db.close()
    return _rowtoepisode(showname, rows[0])


def getnextepisode(showname):
    """ Get the first unwatched episode of a show.

    """
    db = _getdbcon()
    c = db.cursor()
    # Find the first unwatched show by using SQL ordering
    sql = """
        SELECT e.number, e.name, e.airdate, e.description, e.watched, e.season_number
        FROM shows AS s, episodes AS e
        WHERE s.name = ?
          AND s.id = e.show_id
          AND e.watched = 0
        ORDER BY e.number, e.season_number ASC
        """
    c.execute(sql, (showname,))
    row = c.fetchone()
    db.close()
    return _rowtoepisode(showname, row)


def markwatched(episode, markprevious=False, watched=True):
    """ Set the watched-attribute of one and/or all previous episodes of show.

    """
    if not episodeexists(showname=episode.showname,
                         seasonnum=episode.seasonnumber,
                         episodenum=episode.number):
        print "{ep} doesn't exist in database!".format(episode.getprettyname())
        return
    # Episode exists in DB.
    db = _getdbcon()
    c = db.cursor()
    sql = """
        UPDATE episodes
           SET watched = ?
           WHERE season_number {eq} ?
             AND number {eq} ?
             AND show_id = ?
        """.format(eq="<=" if markprevious else "=")
    c.execute(sql, (watched, episode.seasonnumber, episode.number,
                    _getshowid(episode.showname)))
    db.commit()
    db.close()


def updateshow(showname):
    db = _getdbcon()
    # imdb
    db.close()


def showexists(showname):
    """ Tell if a show already exists in the database.

    """
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


def _getshowid(showname):
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
    return rows[0][0]


def episodeexists(showname, seasonnum, episodenum):
    db = _getdbcon()
    c = db.cursor()
    sql = """
        SELECT *
        FROM shows AS s, episodes AS e
        WHERE s.name = ?
          AND s.id = e.show_id
          AND e.season_number = ?
          AND e.number = ?
        """
    c.execute(sql, (showname, seasonnum, episodenum))
    rows = c.fetchall()
    assert len(rows) in (0, 1), "Duplicate episodes in database!"
    return len(rows) == 1


def _rowtoshow(row):
    pass


def _rowtoepisode(showname, row):
    """ Convert a row from sqlite to an instance of Episode.
    Assumes that 'row' is a listy type with episode information in the
    following order:
    [number, name, airdate, description, watched, seasonnumber]

    """
    return Episode(number=row[0],
                   name=row[1],
                   airdate=datetime.strptime(row[2], SQL_DATE_FORMAT).date(),
                   description=row[3],
                   watched=row[4] == 1,
                   seasonnumber=row[5],
                   showname=showname)


def _storeshow(show):
    """ Store a show (instance of Show).

    """
    if show is None:
        return
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
        _storeepisodes(show.name, season.episodes)


def _storeepisodes(showname, episodes):
    """ Store a listy of episodes in the database (instances of Episode).

    """
    if not all(map(lambda e: e.showname == showname, episodes)):
        print("Not all episodes belong to the same show! Will not store the episodes.")
        return
    if not showexists(showname):
        show = imdb.getshow(showname)
        if show is None:
            print "Couldn't find show on IMDB."
            return
        _storeshow(show)
    showid = _getshowid(showname)
    sql = """
        INSERT INTO episodes (show_id, number, name, airdate, description, watched, season_number)
        VALUES (?, ?, ?, ?, ?, ?, ?);
        """
    episodetuples = map(lambda e: (showid, e.number, e.name, e.airdate, e.description,
                                   e.watched, e.seasonnumber),
                        episodes)
    db = _getdbcon()
    c = db.cursor()
    c.executemany(sql, episodetuples)
    db.commit()
    db.close()
