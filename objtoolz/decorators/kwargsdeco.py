'''
    objtoolz.decorators.kwargsdeco
    `````````````````````````````````
    Decorators that allow provide keyword arguments to decorators when wrapping
'''

from toolz import curry
from ..descriptors.undescriptor import Undescriptor
from ..compat import update_wrapper

__all__ = ('method_kwargs_decorator',)


def kwargs_decorator(deco):
    """Allows creating decorators that accept optional keyword arguments.

    ..code-block:: python

        @kwargs_decorator
        def print_before(func, pre='Hello!')
            @wraps(func)
            def wrapper(*a, **k):
                print(pre)
                return func(*a, **k)
            return wrapper

        @print_before(pre='Whatup!')
        def thing():
            pass

        @print_before
        def other_thing():
            pass
    """
    return update_wrapper(curry(deco), deco)


def method_kwargs_decorator(method):
    """Allows using kwargs_decorator to wrap methods and potentially other
    descriptors.
    """
    return Undescriptor(kwargs_decorator, method)
