from .base import Descriptor

__all__ = ('Instance',)


class Instance(Descriptor):
    """Helper descriptor to allow attaching an instance of a class to the class
    itself as a class attribute. Might be helpful someday. The created instance
    is cached and stored inside the descriptor. It is possible to store multiple
    instances on the class, if wanted.

    ..code-block:: python
        class Thing(object):
            frob = Instance()

    Once the class is built, `Thing.frob` is a cached instance of `Thing` itself.

    Additionally, a *specific* instance can be created by passing args and kwargs
    to Instance:

    ..code-block:: python
        class Frob(object):
            default = Instance(name='Default Frob', value=1)

            def __init__(self, value, name):
                self.name = name
                self.value = value

    The instance is created and stored with those values.
    """

    def __init__(self, *args, **kwargs):
        self._args = args
        self._kwargs = kwargs
        self._inst = None

    def __get__(self, _, cls):
        if self._inst is None:
            self._inst = cls(*self._args, **self._kwargs)
        return self._inst
