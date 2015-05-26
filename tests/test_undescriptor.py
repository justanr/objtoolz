from objtoolz.descriptors.undescriptor import undescript, Undescriptor
import pytest


class BadDescriptor(object):
    def __init__(self, method):
        self.method = method

    # purposely don't resolve to a bound method
    def __get__(self, inst, cls):
        return self.method


def just_call_it(func):
    def wrapper(*a, **k):
        return func(*a, **k)
    return wrapper


def test_undescript_with_classmethod():
    class Dummy(object):
        @classmethod
        def something(cls, a):
            return (cls, a)

    # avoid activating descriptor protocol
    descripted = Dummy.__dict__['something']
    undescripted = undescript(descripted, None, Dummy)

    # classmethod is not callable itself
    # but the underlying method is
    assert callable(undescripted)
    assert undescripted(1) == (Dummy, 1)


def test_undescript_with_staticmethod():
    class Dummy(object):
        @staticmethod
        def something(a):
            return a

    # avoid activating descriptor protocol
    descripted = Dummy.__dict__['something']
    undescripted = undescript(descripted, None, Dummy)

    # staticmethod is not callable itself
    # but the underlying method is
    assert callable(undescripted)
    assert undescripted(1) == 1


def test_undescript_with_property():
    class Dummy(object):
        @property
        def something(self):
            return self

    d = Dummy()

    descripted = Dummy.__dict__['something']
    undescripted = undescript(descripted, d, Dummy)

    assert undescripted is d


def test_undescript_with_bad_descriptor():
    class Dummy(object):
        @BadDescriptor
        @classmethod
        def something(cls, a):
            return (cls, a)

    d = Dummy()
    descripted = Dummy.__dict__['something']
    undescripted = undescript(descripted, d, Dummy)

    assert callable(undescripted)
    assert undescripted(1) == (Dummy, 1)


def test_undescriptor_with_classmethod():
    class Dummy(object):
        @Undescriptor(just_call_it)
        @classmethod
        def something(cls, a):
            return cls, a

    assert Dummy.something(1) == (Dummy, 1)


def test_undescriptor_with_staticmethod():
    class Dummy(object):
        @Undescriptor(just_call_it)
        @staticmethod
        def something(a):
            return a

    assert Dummy.something(1) == (1)


def test_undescriptor_with_property():
    class Dummy(object):
        @Undescriptor(str.upper)
        @property
        def something(self):
            return self.__class__.__name__

    assert Dummy().something == 'DUMMY'


def test_undescriptor_with_bad_descriptor():
    class Dummy(object):
        @Undescriptor(just_call_it)
        @BadDescriptor
        @staticmethod
        def something(a):
            return a

    assert Dummy.something(1) == 1


def test_load_undescriptor_at_init():
    class Dummy(object):
        @classmethod
        def something(cls, a):
            return cls, a

        wrapped = Undescriptor(just_call_it, something)

    assert Dummy.wrapped(1) == (Dummy, 1)


def test_loaded_undescriptor_errors():
    with pytest.raises(AttributeError) as excinfo:
        class Dummy(object):
            def something(self, a):
                return self, a

            @Undescriptor(just_call_it, something)
            @classmethod
            def otherthing(*a):
                pass

    assert "Method already loaded" == str(excinfo.value)
