'''
    objtoolz.descriptors.hybridmappingstore
    ```````````````````````````````````````
    Descriptor to provide restricted to a key-value store based on if
    a class or instance is accessing the attribute.
'''

from .base import Descriptor

__all__ = ('HybridMappingStore',)


class HybridMappingStore(Descriptor):
    """Allows creating a key-value store that has different access rights
    based on if the class or an instance is accessing it. The class can access
    all of its instances' data, but an instance can only reach its own data.
    """

    def __init__(self, valuestore, default=None):
        self._valuestore = valuestore
        self._default = default

    def __get__(self, inst, cls):
        if inst is None:
            return self._valuestore
        else:
            return self._valuestore.setdefault(inst, self._default)

    def __set__(self, inst, value):
        self._valuestore[inst] = value

    def __delete__(self, inst):
        self._valuestore.pop(inst, None)
