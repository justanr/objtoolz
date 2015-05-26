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
    """
    def __call__(cls, *args, **kwargs):
        try:
            return cls.__inst
        except AttributeError:
            cls.__inst = super(Singleton, cls).__call__(*args, **kwargs)
            return cls.__inst
