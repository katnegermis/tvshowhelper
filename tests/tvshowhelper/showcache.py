from os.path import join, abspath, dirname
import sys

here = lambda *args: join(abspath(dirname(__file__)), *args)
root = here("..", "..")
sys.path.append(root)

import unittest
from datetime import date

from tvshowhelper import showcache
from tvshowhelper.classes.show import Show
from tvshowhelper.classes.episode import Episode


class Testshowcache(unittest.TestCase):

    def setUp(self):
        """ Create a test show and add 10 test episodes to it.

        """
        # Create test show.
        self.showname = 'The Test Show'
        self.show = Show(name=self.showname)
        showcache._storeshow(self.show)

        self.seasonnumber = 1
        # Create test episodes.
        # Every second episode, starting from episode 0, is unwatched.
        self.episodes = self._createtestepisodes(seasonnumber=self.seasonnumber,
                                                 numepisodes=10,
                                                 watched=lambda epnum: epnum % 2 == 1)
        showcache._storeepisodes(self.showname, self.episodes)

    def tearDown(self):
        """ Delete test show and its' episodes.

        """
        db = showcache._getdbcon()
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

    def _createtestepisodes(self, seasonnumber, numepisodes, watched):
        """ Create test episodes.
            Every second episode, starting from episode 0, is unwatched.

            `watched` is a function that takes as input the number of an episode
            and returns True if the episode should be marked as watched.

        """
        episodes = []
        for episodenumber in range(10):
            ep = Episode(number=episodenumber,
                         name="S{s}E{e}".format(s=seasonnumber, e=episodenumber),
                         airdate=date.today(),
                         description="Description of episode {ep} of {name}".format(ep=episodenumber, name=self.showname),
                         watched=watched(episodenumber),  # Mark every second as unwatched
                         seasonnumber=seasonnumber,
                         showname=self.showname)
            episodes.append(ep)
        return episodes

    def test_getepisode_existing(self):
        """ Verify that we can retrieve the episode we ask for.

        """
        # We can find all episodes of the show we created.
        for epnum in range(len(self.episodes)):
            episode = showcache.getepisode(showname=self.showname, seasonnum=1,
                                             episodenum=epnum)
            self.assertEquals(episode.seasonnumber, self.seasonnumber)
            self.assertEquals(episode.number, epnum)
            self.assertEquals(episode.showname, self.showname)

    def test_getepisode_non_existing(self):
        """ Verify that we don't retrieve episodes that don't exist.

        """
        # We can't find an episode that doesn't exist.
        nonexistentepisode = showcache.getepisode(showname=self.showname,
                                                    seasonnum=self.seasonnumber,
                                                    episodenum=100)
        self.assertIsNone(nonexistentepisode)

        # We can't find an episode in a show that doesn't exist.
        nonexistentshow = showcache.getepisode(showname="no such show",
                                                 seasonnum=self.seasonnumber,
                                                 episodenum=0)
        self.assertIsNone(nonexistentshow)

    def test_showexists(self):
        """ Verify that we find shows that exist, and can't find shows that
        don't exist.

        """
        # We can find a show that exists.
        self.assertTrue(showcache.showexists(self.showname))

        # We can't find a show that doesn't exist.
        self.assertFalse(showcache.showexists('nonexistent show title'))

        # Show names are case sensitive.
        self.assertFalse(showcache.showexists(self.showname.lower()))
        self.assertFalse(showcache.showexists(self.showname.upper()))

    def test_episodeexists(self):
        """ Verify that we find episodes that exist, and can't find episodes
        that don't exist.

        """
        # We can find show that exists.
        self.assertTrue(showcache.episodeexists(self.showname,
                                                  seasonnum=self.seasonnumber,
                                                  episodenum=0))
        # We can't find episode that doesn't exist.
        self.assertFalse(showcache.episodeexists(self.showname,
                                                   seasonnum=self.seasonnumber,
                                                   episodenum=999))

        # We can't find episode in season that doesn't exist.
        self.assertFalse(showcache.episodeexists(self.showname,
                                                   seasonnum=self.seasonnumber + 1,
                                                   episodenum=0))

        # We can't find episode from show that doesn't exist.
        self.assertFalse(showcache.episodeexists("nonexistent show",
                                                   seasonnum=self.seasonnumber,
                                                   episodenum=999))

    def test_getnextepisode_single_season(self):
        """ Verify that we get the first unwatched episode from the series.

            Relies on `markwatched` to work correctly.

        """

        # We find first unwatched episode (Episode 0)
        episode = showcache.getnextepisode(self.showname)
        self.assertEquals(episode.seasonnumber, self.seasonnumber)
        self.assertEquals(episode.number, 0)

        # We continue to find the same episode since it hasn't been marked watched (Episode 0)
        for __ in range(100):
            episode = showcache.getnextepisode(self.showname)
            self.assertEquals(episode.seasonnumber, self.seasonnumber)
            self.assertEquals(episode.number, 0)

        # We find next unwatched episode (Episode 2), since `the previous first`
        # is being marked as watched.
        showcache.markwatched(episode, markprevious=False, watched=True)
        episode = showcache.getnextepisode(self.showname)
        self.assertEquals(episode.seasonnumber, self.seasonnumber)
        self.assertEquals(episode.number, 2)

    def test_getnextepisode_multiple_seasons(self):
        """ Verify that we get the first unwatched episode of the series,
        even though there are multiple seasons of the show.

            Relies on `markwatched` to work correctly.

        """
        # Set up: Create a 2nd season of test episodes, of which none
        # of the episodes are watched.
        episodes = self._createtestepisodes(seasonnumber=2, numepisodes=10,
                                            watched=lambda e: False)
        showcache._storeepisodes(self.showname, episodes)

        # The first unwatched episode should be episode 0 from season 1
        episode = showcache.getnextepisode(self.showname)
        self.assertEquals(episode.seasonnumber, 1)
        self.assertEquals(episode.number, 0)

        # We mark all episodes of the first season to be watched
        episode = showcache.getepisode(self.showname, seasonnum=1,
                                         episodenum=len(self.episodes) - 1)
        showcache.markwatched(episode, markprevious=True, watched=True)

        # The first unwatched episode should now be episode 0 from season 2.
        episode = showcache.getnextepisode(self.showname)
        self.assertEquals(episode.seasonnumber, 2)
        self.assertEquals(episode.number, 0)

    def test_markwatched_single(self):
        """ Verify that we can mark an unwatched episode watched, and vice versa.

            Relies on `getepisode` to work correctly.

        """
        epnum = 0
        # Episode is unwatched
        episode = showcache.getepisode(self.showname, seasonnum=self.seasonnumber,
                                         episodenum=epnum)
        self.assertFalse(episode.watched)

        # We can mark episode watched
        showcache.markwatched(episode, markprevious=False, watched=True)
        episode = showcache.getepisode(self.showname, seasonnum=self.seasonnumber,
                                         episodenum=epnum)
        self.assertTrue(episode.watched)

        # We can mark episode unwatched
        showcache.markwatched(episode, markprevious=False, watched=False)
        episode = showcache.getepisode(self.showname, seasonnum=self.seasonnumber,
                                         episodenum=epnum)
        self.assertFalse(episode.watched)

    def test_markwatched_mark_previous(self):
        """ Verify that we can mark previous episodes.

            Relies on `getepisode` to work correctly.

        """
        half = (len(self.episodes) - 1) // 2
        # Mark all episodes watched
        episode = showcache.getepisode(self.showname, seasonnum=self.seasonnumber,
                                         episodenum=len(self.episodes) - 1)
        showcache.markwatched(episode, markprevious=True, watched=True)

        # Mark first half of episodes unwatched
        episode = showcache.getepisode(self.showname, seasonnum=self.seasonnumber,
                                         episodenum=half)
        showcache.markwatched(episode, markprevious=True, watched=False)

        # First half is unwatched
        for epnum in range(half + 1):
            episode = showcache.getepisode(self.showname, seasonnum=self.seasonnumber,
                                             episodenum=epnum)
            self.assertFalse(episode.watched)

        # Second half is watched
        for epnum in range(half + 1, len(self.episodes)):
            episode = showcache.getepisode(self.showname, seasonnum=self.seasonnumber,
                                             episodenum=epnum)
            self.assertTrue(episode.watched)

if __name__ == '__main__':
    unittest.main()
