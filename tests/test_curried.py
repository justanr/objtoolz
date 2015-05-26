from toolz import curry
from objtoolz.metas.curried import Curried
from objtoolz.compat import with_metaclass


class Dummy(with_metaclass(Curried)):
    accessible = True

    def __init__(self, a, b, c):
        self.a, self.b, self.c = a, b, c

    @classmethod
    def clsmethod(cls):
        return True


def test_all_at_once_creation():
    assert isinstance(Dummy(1, 2, 3), Dummy)


def test_partial_instantiation():
    d = Dummy(1, b=2)
    assert isinstance(d, curry)
    assert d.func.__wrapped__ is Dummy
    assert d.args == (1,)
    assert d.keywords == {'b': 2}


def test_partial_to_full_instantiation():
    d = Dummy(1)
    assert isinstance(d(2, 3), Dummy)


def test_dont_shadow_class_level_stuff():
    assert Dummy.accessible
    assert Dummy.clsmethod()


def test_inherit_curryness():
    class InheritedCurry(Dummy):
        pass

    d = InheritedCurry(1, b=2)
    assert isinstance(d, curry)
    assert d.func.__wrapped__ is InheritedCurry
    assert d.args == (1,)
    assert d.keywords == {'b': 2}
