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
        """ Create a test show and add 10 test episodes to it.

        """
        # Create test show.
        self.showname = 'The Test Show'
        self.show = Show(name=self.showname)
        seriescache._storeshow(self.show)

        self.seasonnumber = 1
        # Create test episodes.
        # Every second episode, starting from episode 0, is unwatched.
        self.episodes = []
        for epnum in range(10):
            ep = Episode(number=epnum,
                         name="Episode " + str(epnum),
                         airdate=date.today(),
                         description="Description of episode {ep} of {name}".format(ep=epnum, name=self.showname),
                         watched=epnum % 2 == 1,  # Mark every second as unwatched
                         seasonnumber=self.seasonnumber,
                         showname=self.showname)
            self.episodes.append(ep)
        seriescache._storeepisodes(self.showname, self.episodes)

    def tearDown(self):
        """ Delete test show and its' episodes.

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
        # Delete episodes.
        episodes = map(lambda e: (e.number, e.name, e.airdate, e.description,
                                  e.watched, e.seasonnumber),
                       self.episodes)
        c.executemany(sql, episodes)

        # Delete show.
        c.execute("DELETE FROM shows WHERE name = ?", (self.showname,))

        db.commit()
        db.close()

    def test_getepisode(self):
        # We can find all episodes of the show we created.
        for epnum in range(len(self.episodes)):
            episode = seriescache.getepisode(showname=self.showname, seasonnum=1,
                                             episodenum=epnum)
            self.assertEquals(episode.seasonnumber, self.seasonnumber)
            self.assertEquals(episode.number, epnum)
            self.assertEquals(episode.showname, self.showname)

        # We can't find an episode that doesn't exist.
        nonexistentepisode = seriescache.getepisode(showname=self.showname,
                                                    seasonnum=self.seasonnumber,
                                                    episodenum=len(self.episodes))
        self.assertIsNone(nonexistentepisode)

        # We can't find an episode in a show that doesn't exist.
        nonexistentshow = seriescache.getepisode(showname="no such show",
                                                 seasonnum=self.seasonnumber,
                                                 episodenum=epnum)
        self.assertIsNone(nonexistentshow)

    def test_showexists(self):
        # We can find a show that exists.
        self.assertTrue(seriescache.showexists(self.showname))

        # We can't find a show that doesn't exist.
        self.assertFalse(seriescache.showexists('nonexistent show title'))

        # Show names are case sensitive.
        self.assertFalse(seriescache.showexists(self.showname.lower()))
        self.assertFalse(seriescache.showexists(self.showname.upper()))

    def test_episodeexists(self):
        # We can find show that exists.
        self.assertTrue(seriescache.episodeexists(self.showname,
                                                  seasonnum=self.seasonnumber,
                                                  episodenum=0))
        # We can't find episode that doesn't exist.
        self.assertFalse(seriescache.episodeexists(self.showname,
                                                   seasonnum=self.seasonnumber,
                                                   episodenum=999))

        # We can't find episode in season that doesn't exist.
        self.assertFalse(seriescache.episodeexists(self.showname,
                                                   seasonnum=self.seasonnumber + 1,
                                                   episodenum=0))

        # We can't find episode from show that doesn't exist.
        self.assertFalse(seriescache.episodeexists("nonexistent show",
                                                   seasonnum=self.seasonnumber,
                                                   episodenum=999))

    def test_getnextepisode(self):
        # We find first unwatched episode (Episode 0)
        episode = seriescache.getnextepisode(self.showname)
        self.assertEquals(episode.seasonnumber, self.seasonnumber)
        self.assertEquals(episode.number, 0)

        # We find the same episode since it hasn't been marked watched (Episode 0)
        for __ in range(100):
            episode = seriescache.getnextepisode(self.showname)
            self.assertEquals(episode.seasonnumber, self.seasonnumber)
            self.assertEquals(episode.number, 0)

        # We find next unwatched episode (Episode 2), since first has been marked watched.
        seriescache.markwatched(episode, markprevious=False, watched=True)
        episode = seriescache.getnextepisode(self.showname)
        self.assertEquals(episode.seasonnumber, self.seasonnumber)
        self.assertEquals(episode.number, 2)

    def test_markwatched_single(self):
        epnum = 2
        # Episode is unwatched
        episode = seriescache.getepisode(self.showname, seasonnum=self.seasonnumber,
                                         episodenum=epnum)
        self.assertFalse(episode.watched)

        # We can mark episode watched
        seriescache.markwatched(episode, markprevious=False, watched=True)

        # Episode has been marked watched
        episode = seriescache.getepisode(self.showname, seasonnum=self.seasonnumber,
                                         episodenum=epnum)
        self.assertTrue(episode.watched)

        # We can mark episode unwatched
        seriescache.markwatched(episode, markprevious=False, watched=False)

        # Episode has been marked unwatched
        episode = seriescache.getepisode(self.showname, seasonnum=self.seasonnumber,
                                         episodenum=epnum)
        self.assertFalse(episode.watched)

    def test_markwatched_mark_previous(self):
        half = (len(self.episodes) - 1) // 2
        # Mark all episodes watched
        episode = seriescache.getepisode(self.showname, seasonnum=self.seasonnumber,
                                         episodenum=len(self.episodes) - 1)
        seriescache.markwatched(episode, markprevious=True, watched=True)

        # Mark first half of episodes unwatched
        episode = seriescache.getepisode(self.showname, seasonnum=self.seasonnumber,
                                         episodenum=half)
        seriescache.markwatched(episode, markprevious=True, watched=False)

        # First half is unwatched
        for epnum in range(half + 1):
            episode = seriescache.getepisode(self.showname, seasonnum=self.seasonnumber,
                                             episodenum=epnum)
            self.assertFalse(episode.watched)

        # Second half is watched
        for epnum in range(half + 1, len(self.episodes)):
            episode = seriescache.getepisode(self.showname, seasonnum=self.seasonnumber,
                                             episodenum=epnum)
            self.assertTrue(episode.watched)

if __name__ == '__main__':
    unittest.main()
