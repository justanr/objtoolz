"""
    objtoolz.descriptors.undescript
    ```````````````````````````````
    Helpers for boring through layers of descriptors to get the underlying
    method
"""
from .base import Descriptor
from ..compat import update_wrapper, wraps

__all__ = ('undescript', 'Undescriptor')


def undescript(method, inst, cls):
    """By repeatedly feeding an instance and class to a method's __get__ method,
    the descriptor protocol is activated and eventually Python begins just
    returning the actual method instead of the descriptors around it.

    However, a simple check is not enough. A comparison between the current
    level and "the next level down" is needed. If the current layer and next
    layer are the same, the original method has been reached and bound.
    """
    deeper_down = None

    while deeper_down is not method:
        method = method.__get__(inst, cls)
        deeper_down = method.__get__(inst, cls)

    return method


class Undescriptor(Descriptor):
    """This descriptor solves the problem of needing to wrap descriptors.
    Given a decorator as its initial argument, when it is reached in the
    decorator chain, it's __call__method accepts whatever has been returned
    below it. And the __get__ method resolves the descriptor protocol to a
    bound method, applies the decorator, and returns a callable closure instead.


    .. code-block:: python
        def report_and_call(func):
            def wrapper(*a, **k):
                print("Called {!r} with {!r} and {!r}".format(func, a, k))
                return func(*a, **k)
            return wrapper


        class Thing(object):
            def __init__(self, raw_frob):
                self.frob = raw_frob // 3

            @Undescriptor(report_and_call)
            @classmethod
            def from_frob(cls, frob):
                return cls(frob*3)

        Thing.from_frob(3)
        "Called <bound method type.from_frob of <class '__main__.Thing'>>
        with (3,) and {}"
        <__main__.Thing at 0x7fe50857de80>

    Even though ``report_and_call`` knows nothing of descriptors, it's still
    very capable of wrapping with a detour through ``Undescriptor``

    Optionally, a method can be provided at initialization as well for an all
    at once deal.

    .. code-block:: python

        def my_deco(func):
            ...

        def wrap_method_with_deco(method):
            return Undescriptor(my_deco, method)

        class Test:
            @wrap_method_with_deco
            @classmethod
            def some_method(cls, *things):
                ...
    """
    # TODO: provide some sort of cache so the method resolution doesn't need
    #       to be preformed on *every* look up?
    def __init__(self, decorator, method=None):
        self._decorator = decorator
        self._method = method
        # pose as decorator
        update_wrapper(self, decorator)

    def __repr__(self):
        return repr(self._decorator)

    def __call__(self, method):
        """Load a method into the instance
        """
        if self._method is not None:
            raise AttributeError("Method already loaded")

        self._method = method
        return self

    def __get__(self, inst, cls):
        """Resolve wrapped method to a bound method of some sort
        and then apply the decorator to that particular bound method
        and provide a wrapper to invoke it.
        """
        if self._method is None:
            raise AttributeError("No method loaded")

        method = undescript(self._method, inst, cls)

        @wraps(method)
        def wrapper(*a, **k):
            return self._decorator(method)(*a, **k)

        # cause closure to pose as wrapped method
        return wrapper
