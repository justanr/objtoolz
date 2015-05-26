'''
    objtoolz.metas
    ``````````````
    Metaclasses for aiding in building classes
'''

from .curried import *
from .final import *
from .memoize import *
from .namedmeta import *
from .singleton import *


class CurriedMemoized(Curried, Memoized):
    """Metaclass to allow curried instantiation and when an object is returned,
    it is Memoized.
    """
    pass


def with_metaclass(meta, *bases, **kwargs):
    """Allows inheriting from an anonymous object with the specified metaclass.
    If a metaclass allows optional or required keyword arguments they can be
    provided in this function.

    Modified from Armin Ronacher's spin on six.py's with_metaclass
    """
    class metaclass(meta):
        __call__ = type.__call__
        __init__ = type.__init__

        def __new__(cls, name, this_bases, d):
            if this_bases is None:
                return type.__new__(cls, name, (), d)
            return meta(name, bases, d, **kwargs)

    return metaclass('temporary_class', None, {})
