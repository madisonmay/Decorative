"""
Decorator for in-memory caching the results of function calls
"""
import inspect
from collections import OrderedDict

from decorator import decorator


class QueueDict(OrderedDict):

    def __init__(self, *args, **kwargs):
        self.max_size = kwargs.pop('max_size')
        OrderedDict.__init__(self, *args, **kwargs)

    def __setitem__(self, *args, **kwargs):
        OrderedDict.__setitem__(self, *args, **kwargs)
        self._limit_size()

    def __getitem__(self, key):
        value = OrderedDict.__getitem__(self, key)
        OrderedDict.__setitem__(self, key, value)
        return value

    def _limit_size(self):
        if self.max_size is not None:
            while len(self) > self.max_size:
                self.popitem(last=False)


def cache(max_size=None):
    """
    Cache the results of computationally expensive operations in memory.
    Removes the least recently used items

    Example usage:
    
    ```
    import time

    @cache
    def long_division(a, b):
        time.sleep(1)
        return a / b

    uncached_start = time.time()
    result = long_division(1., 2.)
    uncached_end = time.time()
    uncached_time = uncached_end - uncached_start

    cached_start = time.time()
    result = long_division(1., 2.)
    cached_end = time.time()
    cached_time = cached_end - cached_start

    assert cached_time < uncached_time
    ```

    """

    lru_cache = QueueDict(max_size=max_size)

    @decorator
    def wrapper(fn, *args, **kwargs):

        keyword_arguments = inspect.getcallargs(fn, *args, **kwargs)

        try:    
            hashed = hash(tuple(keyword_arguments.items()))
        except TypeError:
            # arguments are not hashable
            raise TypeError(
                "The cache decorator only accepts immutable arguments."
            )

        try:
            # results are cached
            return lru_cache[hashed]
        except KeyError:
            # results not cached
            value = fn(*args, **kwargs)
            lru_cache[hashed] = value
            return value

    return wrapper
