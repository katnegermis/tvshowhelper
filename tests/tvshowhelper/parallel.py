import unittest
from os.path import dirname, join, abspath
import sys
from datetime import datetime

here = lambda *args: join(abspath(dirname(__file__)), *args)
root = here("..", "..")
sys.path.append(root)

from tvshowhelper.parallel import parallel_map


class TestParallel(unittest.TestCase):

    def test_map(self):
        def _square(x):
            return x + 1

        numbers = range(1000)

        print(datetime.now())

        squared_numbers = map(_square, numbers)

        print(datetime.now())

        results = parallel_map(_square, numbers, 500)

        print(datetime.now())

        self.assertTrue(results == squared_numbers)

if __name__ == '__main__':
    unittest.main()
