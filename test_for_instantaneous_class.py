import pytest
import ecg_data

def test_for_instantaneous_class():
    """Unit test for checking instantaneous functionality
    checks for out of bounds and default heart rate

    """

    myObject = Ecg_data('full_test.csv')

    assert myObject.instantHr('full_test.csv',inst = True) == 80

    with pytest.raises(ValueError):
        myObject.instantHr('full_test.csv',250000, inst = True)
