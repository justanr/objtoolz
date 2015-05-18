from objtoolz.metas.final import Final
import pytest


def test_cant_inherit_from_final():
    class FinalTest(object):
        pass

    FinalTest = Final('FinalTest', (FinalTest,), {})

    with pytest.raises(TypeError) as err:
        class SubclassedFinalTest(FinalTest):
            pass

    assert 'Attempting to inherit from final class' in str(err.value)
