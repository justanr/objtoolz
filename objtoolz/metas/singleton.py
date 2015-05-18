'''
    objtoolz.metas.singleton
    ````````````````````````
    Metaclass that allows only one instance of a class.
'''

from .final import Final

__all__ = ('Singleton',)


class Singleton(Final):
    """Singleton metaclass that only allows one instance of a class. Singletons
    are also considered Final. If there's only one instance of a class, no
    subclasses should exist.

    As with Final itself, this metaclass cannot be used with the "with_metaclass"
    helper to create instances, as creating a singleton should be carefully
    considered.
    """
    def __call__(cls, *args, **kwargs):
        return super(Singleton, cls).__call__(*args, **kwargs)
