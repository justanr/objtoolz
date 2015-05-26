from objtoolz.metas import Singleton
from objtoolz.compat import with_metaclass
import pytest


class Dummy(with_metaclass(Singleton)):
    pass


def test_singleton():
    assert Dummy() is Dummy()


def test_cant_inherit_from_singleton():
    with pytest.raises(TypeError) as excinfo:
        class SubDummy(Dummy):
            pass

    assert "Attempting to inherit from final class" in str(excinfo.value)
