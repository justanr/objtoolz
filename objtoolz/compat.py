from toolz.compatibility import *
from functools import partial, WRAPPER_ASSIGNMENTS, WRAPPER_UPDATES

try:
    from functools import singledispatch
except ImportError:
    from singledispatch import singledispatch

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
