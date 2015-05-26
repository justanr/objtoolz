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
