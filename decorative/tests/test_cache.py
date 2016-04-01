import unittest
import time

from decorative import cache


@cache()
def long_division(a, b):
    time.sleep(1)
    return a / b


class CacheTestCase(unittest.TestCase):

    def test_cache(self):
        uncached_start = time.time()
        result = long_division(1., 2.)
        uncached_end = time.time()
        uncached_time = uncached_end - uncached_start

        cached_start = time.time()
        result = long_division(1., 2.)
        cached_end = time.time()
        cached_time = cached_end - cached_start

        assert cached_time < uncached_time
        assert cached_time < 0.01
        assert uncached_time > 1.0
