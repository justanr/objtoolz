"""
    objtoolz.descriptors.nameddescriptor
    ````````````````````````````````````
    Base object for descriptors that automatically link up with their
    attribute name
"""

from .base import Descriptor

__all__ = ('NamedDescriptor',)


class NamedDescriptor(Descriptor):
    """Use with objtoolz.metas.NamedMeta to automatically link up
    the assigned attribute name to the descriptor's name attribute.
    """
    def __init__(self, name=None):
        self.name = name
