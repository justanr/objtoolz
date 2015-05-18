'''
    objtoolz.metas.memoized
    ```````````````````````
    Metaclass that allows memoization of instances
'''

from toolz import memoize
from ..descriptors import HybridMappingStore
from ..compat import wraps


__all__ = ('Memoized',)


def _default_cache_key(args, kwargs):
    """By default, toolz.memoize will only cache positional args if no cache
    key is passed and it can't determine if there's keyword arguments. However,
    this will cause memoize to cache *both* if a cache key func isn't provided.
    """
    return (args or None, frozenset(kwargs.items()) or None)


class Memoized(type):
    # setting these attributes on the metaclass prevents
    # instances from the created classes from accessing them
    # and provides a convenient centralized storage area for them
    # also provide defaults in case an entry is deleted for some reason

    # TODO: Subclassing Memoized without overriding these allows access.
    #       Desired or not?
    _cache = HybridMappingStore({}, default={})
    _cache_key = HybridMappingStore({}, default=_default_cache_key)

    def __new__(mcls, name, bases, attrs, **kwargs):
        return super(Memoized, mcls).__new__(mcls, name, bases, attrs)

    def __init__(cls, name, bases, attrs, key=_default_cache_key, cache=None):
        if cache is None:
            cache = {}
        cls._cache = cache
        cls._cache_key = key
        super(Memoized, cls).__init__(name, bases, attrs)

    def __call__(cls, *args, **kwargs):
        """Memoize actual object instantiation from the created class
        """
        @wraps(cls)
        @memoize(cache=cls._cache, key=cls._cache_key)
        def rememberer(*a, **k):
            return super(Memoized, cls).__call__(*a, **k)
        return rememberer(*args, **kwargs)
