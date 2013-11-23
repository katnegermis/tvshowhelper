import unittest
from os.path import dirname, join, abspath
import sys

here = lambda *args: join(abspath(dirname(__file__)), *args)
root = here("..", "..", "..")
sys.path.append(root)

from tvshowhelper.informationscrapers import google


class TestGoogleModule(unittest.TestCase):

    def test_query(self):
        results = google.query("site:imdb.com how i met your mother")
        self.assertTrue(len(results) == 10)
        self.assertTrue("imdb.com" in results[0]['link'])  # the link should point to imdb.com
        self.assertTrue("tt0460649" in results[0]['link'])  # the link should contain the id of the series

        with self.assertRaises(TypeError):
            google.query([])

if __name__ == '__main__':
    unittest.main()
