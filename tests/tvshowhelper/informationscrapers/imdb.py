import unittest
from os.path import dirname, join, abspath
import sys

here = lambda *args: join(abspath(dirname(__file__)), *args)
root = here("..", "..", "..")
sys.path.append(root)

from tvshowhelper.informationscrapers import imdb
from tvshowhelper.classes.show import Show
from tvshowhelper.classes.season import Season
from tvshowhelper.classes.episode import Episode


class TestImdbModule(unittest.TestCase):
    """ These tests might fail if imdb.com modifies
    the episode-data for 'How I Met Your Mother'.
    """

    def setUp(self):
        self.showname = "How I Met Your Mother"
        self.numepisodes = (22, 22, 20, 24, 24, 24, 24, 24, 11)

    def test_getshow(self):
        show = imdb.getshow(self.showname)
        self.assertIsInstance(show, Show)

        # check that seasons have the following number of episodes
        # this test might fail in the future, if imdb modifies its data
        for i in range(9):
            season = show.getseason(i + 1)
            self.assertIsInstance(season, Season)
            self.assertGreaterEqual(len(season.episodes), self.numepisodes[i])
            for j in range(self.numepisodes[i]):
                self.assertTrue(season.hasepisode(j + 1))
                self.assertIsInstance(season.getepisode(j + 1), Episode)

    def test_getnumseasons(self):
        numseasons = imdb.getnumseasons(self.showname)
        self.assertGreaterEqual(numseasons, 9)

    def test_seasons(self):
        seasons = imdb.getseasons(self.showname)
        self.assertGreaterEqual(len(seasons), 9)

    def test_getepisodes(self):
        episodes = imdb.getepisodes(self.showname, 1)
        self.assertGreaterEqual(len(episodes), self.numepisodes[0])
        for episode in episodes:
            self.assertIsInstance(episode, Episode)

    def test_getnumepisodes(self):
        numepisodes = imdb.getnumepisodes(self.showname, 1)
        self.assertGreaterEqual(numepisodes, self.numepisodes[0])

    def test_mustgivestr(self):
        with self.assertRaises(TypeError):
            imdb.getseasons([])

        with self.assertRaises(TypeError):
            imdb.getnumseasons([])

        with self.assertRaises(TypeError):
            imdb.getepisodes([])

        with self.assertRaises(TypeError):
            imdb.getnumepisodes([])

        with self.assertRaises(TypeError):
            imdb.getshow([])

if __name__ == '__main__':
    unittest.main()
