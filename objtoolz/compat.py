from toolz.compatibility import *
from functools import partial, WRAPPER_ASSIGNMENTS, WRAPPER_UPDATES

try:
    from functools import singledispatch
except ImportError:
    from singledispatch import singledispatch



def with_metaclass(meta, *bases, **kwargs):
    """Allows inheriting from an anonymous object with the specified metaclass.
    If a metaclass allows optional or required keyword arguments they can be
    provided in this function.

    Modified from Armin Ronacher's spin on six.py's with_metaclass
    """
    class metaclass(meta):
        __call__ = type.__call__
        __init__ = type.__init__

        def __new__(cls, name, this_bases, d):
            if this_bases is None:
                return type.__new__(cls, name, (), d)
            return meta(name, bases, d, **kwargs)

    return metaclass('temporary_class', None, {})


def update_wrapper(wrapper, wrapped,
                   assigned=WRAPPER_ASSIGNMENTS, updated=WRAPPER_UPDATES):
    for attr in assigned:
        try:
            value = getattr(wrapped, attr)
        except AttributeError:
            continue
        else:
            setattr(wrapper, attr, value)

    for attr in updated:
        getattr(wrapper, attr, {}).update(getattr(wrapped, attr, {}))

    wrapper.__wrapped__ = wrapped
    return wrapper


def wraps(wrapped, assigned=WRAPPER_ASSIGNMENTS, updated=WRAPPER_UPDATES):
    return partial(update_wrapper, wrapped=wrapped, assigned=assigned, updated=updated) # noqa
