import pytest
import ecg_data

def test_for_instantaneous_class():
    """Unit test for checking instantaneous functionality
    checks for out of bounds and default heart rate

    """

    myHrm = ecg_data.Ecg_data('full_test.csv')

    assert myHrm.instantHr() == 80

    with pytest.raises(ValueError):
        myHrm.instantHr(250)
