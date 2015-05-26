from objtoolz.metas.memoize import Memoized, _default_cache_key
from objtoolz.compat import with_metaclass


def test_default_cache_key():
    assert _default_cache_key((1,), {'b': 2}) == ((1,), frozenset([('b', 2)]))
    assert _default_cache_key((1,), {}) == ((1,), None)
    assert _default_cache_key((), {'b': 2}) == (None, frozenset([('b', 2)]))
    assert _default_cache_key((), {}) == (None, None)


def make_dummy_class(key=None, cache=None):
    class Dummy(with_metaclass(Memoized, cache=cache, key=key)):
        def __init__(self, *args, **kwargs):
            pass
    return Dummy


def test_classes_only_access_own_registry():
    Dummy = make_dummy_class()
    Dummy2 = make_dummy_class()

    d = Dummy(1)
    d2 = Dummy2(1)

    assert d not in Dummy2._cache
    assert d2 not in Dummy._cache
    assert Dummy._cache != Dummy2._cache


def test_specialize_cache_key():
    def cache_key(args, kwargs):
        return str(args) + str(kwargs)

    StringKeyed = make_dummy_class(key=cache_key)
    d = StringKeyed(1, b=2)

    assert "(1,){'b': 2}" in StringKeyed._cache
    assert StringKeyed._cache["(1,){'b': 2}"] is d


def test_specialize_cache_type():
    class MyDict(dict):
        pass

    MyDictCache = make_dummy_class(cache=MyDict())
    assert isinstance(MyDictCache._cache, MyDict)


def test_memoizes():
    Dummy = make_dummy_class()
    d = Dummy(1)
    assert d is Dummy(1)
