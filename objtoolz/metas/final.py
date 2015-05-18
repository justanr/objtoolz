'''
    objtoolz.metas.final
    ````````````````````
    Metaclass for disallowing inheritance
'''

__all__ = ('Final',)


class Final(type):
    """A class with this metaclass cannot be inherited from.

    Note that this class cannot be used with the `with_metaclass` helper
    as it'll create an anonymous Final object. This is intentional as applying
    this class should not be done lightly.
    """
    def __new__(mcls, name, bases, attrs):
        for b in bases:
            if isinstance(b, Final):
                raise TypeError("Attempting to inherit from final class {!r}"
                                .format(b))
        else:
            return super(Final, Final).__new__(mcls, name, bases, attrs)
