'''
    objtoolz.meta.curried
    `````````````````````
    Metaclass to allow currying class instantiation
'''


from toolz import curry
from ..compat import wraps

__all__ = ('Curried',)


class Curried(type):
    """Metaclass for currying object instantiation.
    """

    def __call__(cls, *args, **kwargs):
        """This is where the currying magic occurs. The __call__ in a metaclass
        is analogous to __new__ in a regular class.
        """
        @wraps(cls, updated=[])
        def currier(*a, **k):
            return super(Curried, cls).__call__(*a, **k)
        # there's odd behavior when composed with other
        # metaclasses if done as one function call...
        return curry(currier)(*args, **kwargs)
