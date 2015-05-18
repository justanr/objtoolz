'''
    objtoolz.metas
    ``````````````
    Metaclasses for aiding in building classes
'''

from .curried import *
from .final import *
from .memoize import *
from .singleton import *


class CurriedMemoized(Curried, Memoized):
    """Metaclass to allow curried instantiation and when an object is returned,
    it is Memoized.
    """
    pass


def with_metaclass(meta, *bases):
    """Allows inheriting from an anonymous object with the specified metaclass.
    """
    name = meta.__name__ + 'Base'
    return meta(name, bases, {})
