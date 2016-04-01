import unittest
import time

from decorative import cache

SLEEP_TIME = 0.1


@cache()
def long_division(a, b):
    # it's a pun
    time.sleep(SLEEP_TIME)
    return a / b


@cache()
def dictionary_merger(a, b):
    z = a.copy()
    z.update(b)
    return z


@cache(1)
def limited_cache_long_division(a, b):
    time.sleep(SLEEP_TIME)
    return a / b


class CacheTestCase(unittest.TestCase):

    def test_cache(self):
        uncached_start = time.time()
        long_division(1., 2.)
        uncached_end = time.time()
        uncached_time = uncached_end - uncached_start

        cached_start = time.time()
        long_division(1., 2.)
        cached_end = time.time()
        cached_time = cached_end - cached_start

        assert cached_time < uncached_time
        assert cached_time < SLEEP_TIME
        assert uncached_time > SLEEP_TIME

    def test_invalid_cache(self):
        with self.assertRaises(TypeError):
            dictionary_merger({'a': 1}, {'b': 2})

    def test_limited_cache_size(self):
        limited_cache_long_division(1., 2.)
        limited_cache_long_division(3., 4.)
        
        cached_start = time.time()
        limited_cache_long_division(3., 4.)
        cached_end = time.time()
        cached_time = cached_end - cached_start

        uncached_start = time.time()
        limited_cache_long_division(1., 2.)
        uncached_end = time.time()
        uncached_time = uncached_end - uncached_start

        assert cached_time < uncached_time
        assert cached_time < SLEEP_TIME
        assert uncached_time > SLEEP_TIME
