from .base import Descriptor
from .undescriptor import undescript
from ..compat import update_wrapper, wraps, singledispatch

__all__ = ('SingleDispatch',)


class SingleDispatch(Descriptor):
    """Python 3.4's functools.singledispatch as a descriptor and decorator
    The interface provided is the same as the stock implementation, with the
    added benefit of working as a descriptor for methods as well.
    """

    def __init__(self, func):
        self._dispatcher = singledispatch(func)
        update_wrapper(self, self._dispatcher)

    def __call__(self, *args, **kwargs):
        """When used as a decorator on a function, we'll pass through this
        method.
        """
        return self._dispatcher(*args, **kwargs)

    def __get__(self, inst, cls):
        """When used as a decorator on a method, we'll pass through this
        method. The closure first determines which method it needs and then
        calls the bound version of that method. The great part of that, is
        that this can wrap around a descriptor
        """
        @wraps(self, updated=[])
        def binder(*args, **kwargs):
            method = self._dispatcher.dispatch(args[0].__class__)
            return undescript(method, inst, cls)(*args, **kwargs)
        return binder
