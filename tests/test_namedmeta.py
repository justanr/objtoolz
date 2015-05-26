from objtoolz.compat import with_metaclass
from objtoolz.metas import NamedMeta
from objtoolz.descriptors import NamedDescriptor


def test_autonaming():
    class Dummy(with_metaclass(NamedMeta)):
        some_name = NamedDescriptor()

    assert Dummy.some_name.name == 'some_name'
