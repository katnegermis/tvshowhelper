from os.path import join, abspath, dirname
import sys

here = lambda *args: join(abspath(dirname(__file__)), *args)
root = here("..", "..")
sys.path.append(root)

import unittest
from datetime import date

from tvshowhelper import seriescache
from tvshowhelper.classes.show import Show
from tvshowhelper.classes.episode import Episode


class TestSeriesCache(unittest.TestCase):

    def setUp(self):
        self.showname = 'The Test Show'
        self.episodes = []
        for epnum in range(10):
            ep = Episode(number=epnum,
                         name="Episode " + str(epnum),
                         airdate=date.today(),
                         description="Description of episode {ep} of {name}".format(ep=epnum, name=self.showname),
                         watched=True,
                         seasonnumber=1,
                         showname=self.showname)
            self.episodes.append(ep)
        seriescache._storeepisodes(self.episodes)

    def tearDown(self):
        """ Delete test show and episodes when done testing

        """
        db = seriescache._getdbcon()
        c = db.cursor()
        sql = """
            DELETE FROM episodes
            WHERE number = ?
              AND name = ?
              AND airdate = ?
              AND description = ?
              AND watched = ?
              AND season_number = ?
            """
        episodes = map(lambda e: (e.number, e.name, e.airdate, e.description,
                                  e.watched, e.seasonnumber),
                       self.episodes)
        c.executemany(sql, episodes)

        c.execute("DELETE FROM shows WHERE name = ?", (self.showname,))
        db.commit()
        db.close()

    def test_getepisode(self):
        for epnum in range(10):
            episode = seriescache.getepisode(showname=self.showname, seasonnum=1, episodenum=epnum)
            self.assertTrue(episode.seasonnumber == 1 and episode.number == epnum and
                            episode.showname == self.showname)

        episode = seriescache.getepisode(showname="no such show", seasonnum=1, episodenum=epnum)

    def test_showexists(self):
        self.assertTrue(seriescache.showexists(self.showname))
        self.assertFalse(seriescache.showexists('nonexistent show title'))


if __name__ == '__main__':
    unittest.main()
