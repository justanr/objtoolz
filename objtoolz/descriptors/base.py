"""
    objtoolz.descriptors.base
    `````````````````````````
    Base descriptor class for detecting descriptors via metaclasses
"""

from abc import ABCMeta
from ..compat import with_metaclass

__all__ = ('Descriptor',)


class Descriptor(with_metaclass(ABCMeta)):
    pass

# abstractmethod is actually a function and shouldn't be registered
for desc in (property, classmethod, staticmethod):
    Descriptor.register(desc)
