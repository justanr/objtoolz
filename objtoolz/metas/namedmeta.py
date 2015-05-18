"""
    objtoolz.metas.nameddescriptors
    ```````````````````````````````
    Metaclass for linking instances of objtoolz.descriptors.NamedDescriptor
    to their assigned attributes by name
"""

__all__ = ('NamedMeta',)

from ..descriptors import NamedDescriptor


class NamedMeta(type):
    """Metaclass to detect instances of NamedDescriptor and assigns the
    attribute name to the descriptor's name attribute if it is empty.
    """

    def __new__(mcls, name, bases, attrs):
        for name, value in attrs.items():
            if isinstance(value, NamedDescriptor) and not value.name:
                value.name = name
            return super(NamedMeta, NamedMeta).__new__(mcls, name, bases, attrs)
